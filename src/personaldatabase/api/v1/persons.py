from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from personaldatabase.database.session import get_db
from personaldatabase.models.person_model import PersonModel
from personaldatabase.schemas.person import person_create, person_response, person_update


router = APIRouter(prefix="/persons", tags=["Persons"])


@router.post("/", response_model=person_response, status_code=status.HTTP_201_CREATED)
def create_person(person_in: person_create, db: Session = Depends(get_db)):
    existing_person = db.scalar(
        select(PersonModel).where(PersonModel.email == person_in.email)
    )
    if existing_person:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="En person med denne e-postadressen eksisterer allerede",
        )

    db_person = PersonModel(**person_in.model_dump())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person


@router.get("/search", response_model=list[person_response])
def search_persons(
    q: str = Query(..., min_length=2, description="Søkeord (minst 2 tegn)"),
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=50, description="Maks antall treff som returneres"),
) -> list[PersonModel]:
    search_term = f"%{q.strip()}%"

    query = (
        select(PersonModel)
        .where(
            or_(
                PersonModel.first_name.ilike(search_term),
                PersonModel.last_name.ilike(search_term),
            )
        )
        .order_by(PersonModel.last_name, PersonModel.first_name)
        .limit(limit)
    )

    return list(db.scalars(query).all())

@router.get("/{id}", response_model=person_response)
def get_person(id: int, db: Session = Depends(get_db)):
    person = db.get(PersonModel, id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {id} ble ikke funnet"
        )
    return person


@router.get("/", response_model=list[person_response])
def get_all_persons(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Antall rader å hoppe over"),
    limit: int = Query(
        50, ge=1, le=100, description="Maks antall rader (maks 100)"),
):
    query = select(PersonModel).offset(skip).limit(limit)
    return db.scalars(query).all()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_person(id: int, db: Session = Depends(get_db)):
    person = db.get(PersonModel, id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {id} ble ikke funnet"
        )
    db.delete(person)
    db.commit()

@router.patch("/{id}/toggle-active", response_model=person_response)
def toggle_person_active(id: int, db: Session = Depends(get_db)):
    person = db.get(PersonModel, id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {id} ble ikke funnet",
        )

    person.is_active = not person.is_active
    db.commit()
    db.refresh(person)
    return person

@router.patch("/{id}", response_model=person_response)
def update_person(
    id: int,
    person_in: person_update,
    db: Session = Depends(get_db)
):
    person = db.get(PersonModel, id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {id} ble ikke funnet",
        )

    update_data = person_in.model_dump(exclude_unset=True)
    if "email" in update_data and update_data["email"] != person.email:
        existing = db.scalar(
            select(PersonModel).where(
                PersonModel.email == update_data["email"],
                PersonModel.id != id
            )
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="En person med denne e-postadressen eksisterer allerede",
            )

    # Oppdater feltene på modellen
    for field, value in update_data.items():
        setattr(person, field, value)

    db.commit()
    db.refresh(person)
    return person


