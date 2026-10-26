import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from personaldatabase.core.security import ALGORITHM, SECRET_KEY
from personaldatabase.database.session import get_db
from personaldatabase.models.person_model import PersonModel
from personaldatabase.models.person_verv_model import PersonVervModel
from personaldatabase.models.verv_model import VervModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_person(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> PersonModel:
    """Henter personen som utfører forespørselen basert på JWT Bearer-token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Kunne ikke validere innloggingsdetaljer",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        person_id_str: str | None = payload.get("sub")
        if person_id_str is None:
            raise credentials_exception
        person_id = int(person_id_str)
    except (jwt.InvalidTokenError, ValueError):
        raise credentials_exception

    person = db.get(PersonModel, person_id)
    if not person:
        raise credentials_exception

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
