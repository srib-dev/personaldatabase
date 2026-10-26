from personaldatabase.schemas.filters import PersonFilterParams
from datetime import date
from typing import Annotated

from personaldatabase.crud.person import get_filtered_persons, update_last_signed_contract
from sqlalchemy.util.typing import Literal
from fastapi import Body
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import select, or_
from personaldatabase.database.session import get_db
from personaldatabase.models.course_model import CourseModel
from personaldatabase.models.group_model import GroupModel
from personaldatabase.models.person_course_model import PersonCourseModel
from personaldatabase.models.person_group_model import PersonGroupModel
from personaldatabase.models.person_model import PersonModel
from personaldatabase.models.person_verv_model import PersonVervModel
from personaldatabase.models.verv_model import VervModel
from personaldatabase.core.security import get_password_hash
from personaldatabase.schemas.course import CourseResponse
from personaldatabase.schemas.group import GroupResponse
from personaldatabase.schemas.person import (
    person_create,
    person_response,
    person_update,
)
from personaldatabase.schemas.verv import VervResponse


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

    person_data = person_in.model_dump()
    raw_password = person_data.pop("password", None)
    if raw_password:
        person_data["hashed_password"] = get_password_hash(raw_password)

    db_person = PersonModel(**person_data)
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

@router.post(
    "/bulk",
    response_model=list[person_response],
    status_code=status.HTTP_201_CREATED,
)
def create_persons_bulk(
    persons_in: list[person_create] = Body(..., max_length=100),
    db: Session = Depends(get_db),
):
    if not persons_in:
        return []

    emails = [p.email.lower() for p in persons_in]
    if len(emails) != len(set(emails)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Listen inneholder duplikate e-postadresser",
        )

    existing_emails = set(
        db.scalars(
            select(PersonModel.email).where(PersonModel.email.in_(emails))
        ).all()
    )
    if existing_emails:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Følgende e-poster eksisterer allerede: {', '.join(existing_emails)}",
        )

    db_persons = []
    for p in persons_in:
        p_data = p.model_dump()
        raw_password = p_data.pop("password", None)
        if raw_password:
            p_data["hashed_password"] = get_password_hash(raw_password)
        db_persons.append(PersonModel(**p_data))

    db.add_all(db_persons)
    db.commit()

    for person in db_persons:
        db.refresh(person)

    return db_persons

@router.get("/search", response_model=list[person_response])
def search_persons(
    query: str = Query(..., min_length=2, description="Søkeord (minst 2 tegn)"),
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=50, description="Maks antall treff som returneres"),
) -> list[PersonModel]:
    search_term = f"%{query.strip()}%"

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
def get_persons(
    filters: Annotated[PersonFilterParams, Depends()],
    db: Session = Depends(get_db),
):
    """
    Hent personer med valgfri filtrering på tekst, gruppe, verv, alder,
    og dato for signert kontrakt.
    """
    return get_filtered_persons(db=db, filters=filters)

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


@router.patch(
    "/{id}/contract",
    response_model=person_response,
    summary="Oppdater dato for sist signerte kontrakt",
)
def update_person_contract(
    id: int,
    last_signed_contract: date | None = Query(
        None,
        description="Dato for signert kontrakt (YYYY-MM-DD). Settes til dagens dato hvis tom.",
    ),
    db: Session = Depends(get_db),
):
    """
    Setter ny dato for sist signerte kontrakt. Personen blir aktiv hvis datoen
    gjelder for inneværende semester, ellers inaktiv. Bruk /toggle-active for
    å overstyre manuelt.
    """
    person = db.get(PersonModel, id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {id} ble ikke funnet",
        )

    return update_last_signed_contract(
        db, person, last_signed_contract or date.today()
    )

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

    if "password" in update_data:
        raw_password = update_data.pop("password")
        if raw_password:
            update_data["hashed_password"] = get_password_hash(raw_password)

    # Oppdater feltene på modellen
    for field, value in update_data.items():
        setattr(person, field, value)

    db.commit()
    db.refresh(person)
    return person


@router.get(
    "/{id}/groups",
    response_model=list[GroupResponse],
    summary="Hent alle grupper for en spesifikk person",
)
def get_person_groups(id: int, db: Session = Depends(get_db)):
    person = db.get(PersonModel, id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {id} ble ikke funnet",
        )

    stmt = (
        select(GroupModel)
        .join(PersonGroupModel, GroupModel.id == PersonGroupModel.group_id)
        .where(PersonGroupModel.person_id == id)
    )
    return db.scalars(stmt).all()


@router.get(
    "/{id}/courses",
    response_model=list[CourseResponse],
    summary="Hent alle kurs for en spesifikk person",
)
def get_person_courses(id: int, db: Session = Depends(get_db)):
    person = db.get(PersonModel, id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {id} ble ikke funnet",
        )

    stmt = (
        select(CourseModel)
        .join(PersonCourseModel, CourseModel.id == PersonCourseModel.course_id)
        .where(PersonCourseModel.person_id == id)
    )
    return db.scalars(stmt).all()


@router.get(
    "/{id}/verv",
    response_model=list[VervResponse],
    summary="Hent alle verv for en spesifikk person",
)
def get_person_verv(id: int, db: Session = Depends(get_db)):
    person = db.get(PersonModel, id)
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {id} ble ikke funnet",
        )

    stmt = (
        select(VervModel)
        .join(PersonVervModel, VervModel.id == PersonVervModel.verv_id)
        .where(PersonVervModel.person_id == id)
    )
    return db.scalars(stmt).all()


