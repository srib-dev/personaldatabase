from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from personaldatabase.database.session import get_db
from personaldatabase.models.person_model import PersonModel
from personaldatabase.models.person_verv_model import PersonVervModel
from personaldatabase.models.verv_model import VervModel
from personaldatabase.schemas.person import person_response
from personaldatabase.schemas.person_verv import VervMemberResponse
from personaldatabase.schemas.verv import VervCreate, VervResponse

router = APIRouter(prefix="/verv", tags=["Verv"])


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
    db.delete(verv)
    db.commit()


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
    if not db.get(VervModel, verv_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Verv med ID {verv_id} finnes ikke",
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
    membership = db.get(PersonVervModel, (person_id, verv_id))
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personen har ikke dette vervet",
        )
    db.delete(membership)
    db.commit()
