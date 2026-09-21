from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from personaldatabase.database.session import get_db
from personaldatabase.models.group_model import group_model
from personaldatabase.schemas.group import group_response


router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("/{id}", response_model=group_response)
def get_group(id: int, db: Session = Depends(get_db)):
    group = db.get(group_model, id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gruppe med ID {id} ble ikke funnet"
        )
    return group


@router.get("/", response_model=list[group_response])
def get_all_groups(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Antall rader å hoppe over"),
    limit: int = Query(50, ge=1, le=100, description="Maks antall rader (maks 100)"),
):
    query = select(group_model).offset(skip).limit(limit)
    return db.scalars(query).all()
