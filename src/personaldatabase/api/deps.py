from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from personaldatabase.database.session import get_db
from personaldatabase.models.person_model import PersonModel
from personaldatabase.models.person_verv_model import PersonVervModel
from personaldatabase.models.verv_model import VervModel


#MÅ ENDRES TIL JWT TOKENS FOR PRODUCTION (KUN FOR TESTING)
def get_current_person(
    x_person_id: int = Header(
        ...,
        alias="X-Person-ID",
        description="ID til personen som utfører forespørselen",
    ),
    db: Session = Depends(get_db),
) -> PersonModel:
    """Henter personen som utfører forespørselen basert på X-Person-ID-headeren."""
    person = db.get(PersonModel, x_person_id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ugyldig eller manglende person-identifikator",
        )

    if not person.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Brukerkontoen er deaktivert",
        )

    return person


def require_admin(
    current_person: PersonModel = Depends(get_current_person),
    db: Session = Depends(get_db),
) -> PersonModel:
    """Verifiserer at den innloggede personen har et admin-verv."""
    stmt = (
        select(PersonVervModel)
        .join(VervModel, PersonVervModel.verv_id == VervModel.id)
        .where(
            PersonVervModel.person_id == current_person.id,
            or_(
                VervModel.verv_name.ilike("Admin"),
                VervModel.role.ilike("Admin"),
            ),
        )
    )
    admin_membership = db.scalar(stmt)

    if not admin_membership:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Kun personer med Admin-vervet har tilgang til denne handlingen",
        )

    return current_person
