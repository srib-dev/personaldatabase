from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from personaldatabase.database.session import get_db
from personaldatabase.models.person_model import person_model
from personaldatabase.schemas.person import person_response



router = APIRouter(prefix="/persons", tags=["Persons"])


@router.get("/{id}", response_model=person_response)
def get_personr(id: int, db: Session = Depends(get_db)):
    person = db.get(person_model, id)
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
    limit: int = Query(50, ge=1, le=100, description="Maks antall rader (maks 100)"),
):
    query = select(person_model).offset(skip).limit(limit)
    return db.scalars(query).all()
