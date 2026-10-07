from datetime import timezone
from datetime import datetime
from sqlalchemy import select, or_
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from personaldatabase.database.session import get_db
from personaldatabase.models.group_model import GroupModel
from personaldatabase.models.person_model import PersonModel
from personaldatabase.models.person_group_model import PersonGroupModel
from personaldatabase.schemas.group import GroupCreate, GroupResponse
from personaldatabase.schemas.person_group import (
    GroupMemberAdd,
    GroupMemberResponse,
)



router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post(
    "/",
    response_model=GroupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Opprett en ny gruppe",
)
def create_group(
    group_in: GroupCreate,
    db: Session = Depends(get_db),
):
    # Sjekker om gruppenavnet allerede eksisterer
    existing_group = db.scalar(
        select(GroupModel).where(GroupModel.group_name == group_in.group_name)
    )
    if existing_group:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="En gruppe med dette navnet eksisterer allerede",
        )

    db_group = GroupModel(**group_in.model_dump())
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group



@router.get("/search", response_model=list[GroupResponse])
def search_groups(
    query: str = Query(..., min_length=2, description="Søkeord (minst 2 tegn)"),
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=50, description="Maks antall treff som returneres"),
) -> list[GroupModel]:
    search_term = f"%{query.strip()}%"

    query = (
        select(GroupModel)
        .where(
                GroupModel.group_name.ilike(search_term)
        )
        .order_by(GroupModel.group_name)
        .limit(limit)
    )

    return list(db.scalars(query).all())


@router.get("/{id}", response_model=GroupResponse)
def get_group(id: int, db: Session = Depends(get_db)):
    group = db.get(GroupModel, id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gruppe med ID {id} ble ikke funnet"
        )
    return group


@router.get("/", response_model=list[GroupResponse])
def get_all_groups(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Antall rader å hoppe over"),
    limit: int = Query(50, ge=1, le=100, description="Maks antall rader (maks 100)"),
):
    query = select(GroupModel).offset(skip).limit(limit)
    return db.scalars(query).all()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group(id: int, db: Session = Depends(get_db)):
    group = db.get(GroupModel, id)
    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gruppe med ID {id} ble ikke funnet"
        )
    db.delete(group)
    db.commit()

#legge til person i gruppe
@router.post(
    "/{group_id}/{person_id}",
    response_model=GroupMemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Legg til en person i en gruppe",
)
def add_person_to_group(
    group_id: int,
    person_id: int,
    db: Session = Depends(get_db),
):
    # 1. Sjekk at gruppe og person finnes
    if not db.get(GroupModel, group_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gruppe med ID {group_id} finnes ikke",
        )

    if not db.get(PersonModel, person_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {person_id} finnes ikke",
        )

    # 2. Sjekk om personen allerede er i gruppen
    if db.get(PersonGroupModel, (person_id, group_id)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Personen er allerede medlem av gruppen",
        )

    # 3. Opprett medlemskap med nåværende tidspunkt
    membership = PersonGroupModel(
        person_id=person_id,
        group_id=group_id,
        when_joined_group=datetime.now(timezone.utc),
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership