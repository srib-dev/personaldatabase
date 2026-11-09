from personaldatabase.api.deps import require_admin
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import delete, or_, select
from sqlalchemy.orm import Session

from personaldatabase.database.session import get_db
from personaldatabase.models.person_model import PersonModel
from personaldatabase.models.person_verv_model import PersonVervModel
from personaldatabase.models.verv_model import VervModel
from personaldatabase.schemas.person import person_response
from personaldatabase.schemas.person_verv import VervMemberResponse
from personaldatabase.schemas.verv import VervCreate, VervResponse

router = APIRouter(prefix="/verv", tags=["Verv"], dependencies=[Depends(require_admin)])
#router = APIRouter(prefix="/verv", tags=["Verv"])


def _is_admin_verv(verv: VervModel) -> bool:
    return verv.verv_name.strip().lower() == "admin" or verv.role.strip().lower() == "admin"



@router.post(
    "/",
    response_model=VervResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Opprett et nytt verv",
)
def create_verv(
    verv_in: VervCreate,
    db: Session = Depends(get_db),
):
    if verv_in.verv_name.strip().lower() == "admin" or verv_in.role.strip().lower() == "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kan ikke opprette et nytt verv med navn eller rolle 'Admin'",
        )

    # Sjekker om vervet allerede eksisterer
    existing_verv = db.scalar(
        select(VervModel).where(VervModel.verv_name == verv_in.verv_name)
    )
    if existing_verv:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Et verv med dette navnet eksisterer allerede",
        )

    db_verv = VervModel(**verv_in.model_dump())
    db.add(db_verv)
    db.commit()
    db.refresh(db_verv)
    return db_verv


@router.get("/search", response_model=list[VervResponse])
def search_verv(
    query: str = Query(..., min_length=2, description="Søkeord (minst 2 tegn)"),
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=50, description="Maks antall treff som returneres"),
) -> list[VervModel]:
    search_term = f"%{query.strip()}%"

    stmt = (
        select(VervModel)
        .where(
            or_(
                VervModel.verv_name.ilike(search_term),
                VervModel.role.ilike(search_term),
            )
        )
        .order_by(VervModel.verv_name)
        .limit(limit)
    )

    return list(db.scalars(stmt).all())


@router.get("/{id}", response_model=VervResponse)
def get_verv(id: int, db: Session = Depends(get_db)):
    verv = db.get(VervModel, id)
    if not verv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Verv med ID {id} ble ikke funnet",
        )
    return verv


@router.get("/", response_model=list[VervResponse])
def get_all_verv(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Antall rader å hoppe over"),
    limit: int = Query(50, ge=1, le=100, description="Maks antall rader (maks 100)"),
):
    stmt = select(VervModel).offset(skip).limit(limit)
    return db.scalars(stmt).all()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_verv(id: int, db: Session = Depends(get_db)):
    verv = db.get(VervModel, id)
    if not verv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Verv med ID {id} ble ikke funnet",
        )
    if _is_admin_verv(verv):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin-vervet kan ikke slettes",
        )
    db.delete(verv)
    db.commit()


@router.post(
    "/transfer-admin/{new_admin_id}",
    response_model=VervMemberResponse,
    summary="Overfør Admin-vervet til en annen person",
)
def transfer_admin_verv(
    new_admin_id: int,
    current_admin: PersonModel = Depends(require_admin),
    db: Session = Depends(get_db),
):
    if new_admin_id == current_admin.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Du har allerede Admin-vervet",
        )

    # 1. Finn den nye personen og verifiser at vedkommende kan logge inn
    new_admin = db.get(PersonModel, new_admin_id)
    if not new_admin:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {new_admin_id} finnes ikke",
        )
    if not new_admin.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kan ikke overføre Admin-vervet til en deaktivert bruker",
        )
    if not new_admin.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kan ikke overføre Admin-vervet til en bruker uten passord",
        )

    # 2. Finn Admin-vervet
    admin_verv = db.scalar(
        select(VervModel).where(
            or_(
                VervModel.verv_name.ilike("Admin"),
                VervModel.role.ilike("Admin"),
            )
        )
    )
    if not admin_verv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admin-vervet ble ikke funnet",
        )

    # 3. Fjern nåværende admin(s) og legg til ny admin i samme transaksjon
    db.execute(
        delete(PersonVervModel).where(PersonVervModel.verv_id == admin_verv.id)
    )
    new_membership = PersonVervModel(
        person_id=new_admin_id,
        verv_id=admin_verv.id,
    )
    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)
    return new_membership


# Legge til person i et verv
@router.post(
    "/{verv_id}/members/{person_id}",
    response_model=VervMemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Legg til en person i et verv",
)
def add_person_to_verv(
    verv_id: int,
    person_id: int,
    db: Session = Depends(get_db),
):
    # 1. Sjekk at verv og person finnes
    verv = db.get(VervModel, verv_id)
    if not verv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Verv med ID {verv_id} finnes ikke",
        )

    if _is_admin_verv(verv):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Kun én person kan ha Admin-vervet av gangen. "
                "Bruk /verv/transfer-admin/{new_admin_id} for å overføre vervet."
            ),
        )

    if not db.get(PersonModel, person_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {person_id} finnes ikke",
        )

    # 2. Sjekk om personen allerede har vervet
    if db.get(PersonVervModel, (person_id, verv_id)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Personen har allerede dette vervet",
        )

    # 3. Opprett kobling
    membership = PersonVervModel(
        person_id=person_id,
        verv_id=verv_id,
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


@router.get(
    "/{verv_id}/members",
    response_model=list[person_response],
    summary="Hent alle personer med et spesifikt verv",
)
def get_verv_members(
    verv_id: int,
    db: Session = Depends(get_db),
):
    verv = db.get(VervModel, verv_id)
    if not verv:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Verv med ID {verv_id} ble ikke funnet",
        )

    # JOIN mellom Person og koblingstabellen PersonVerv
    stmt = (
        select(PersonModel)
        .join(PersonVervModel, PersonModel.id == PersonVervModel.person_id)
        .where(PersonVervModel.verv_id == verv_id)
    )

    return db.scalars(stmt).all()


@router.delete(
    "/{verv_id}/members/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Fjern en person fra et verv",
)
def remove_person_from_verv(
    verv_id: int,
    person_id: int,
    db: Session = Depends(get_db),
):
    verv = db.get(VervModel, verv_id)
    if verv and _is_admin_verv(verv):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Kan ikke fjerne Admin direkte. "
                "Bruk /verv/transfer-admin/{new_admin_id} for å overføre vervet til en annen person."
            ),
        )

    membership = db.get(PersonVervModel, (person_id, verv_id))
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personen har ikke dette vervet",
        )
    db.delete(membership)
    db.commit()
