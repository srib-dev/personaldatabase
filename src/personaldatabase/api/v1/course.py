from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from personaldatabase.database.session import get_db
from personaldatabase.models.course_model import CourseModel
from personaldatabase.models.person_course_model import PersonCourseModel
from personaldatabase.models.person_model import PersonModel
from personaldatabase.schemas.course import CourseCreate, CourseResponse
from personaldatabase.schemas.person import person_response
from personaldatabase.schemas.person_course import (
    CourseMemberResponse,
)

router = APIRouter(prefix="/courses", tags=["Courses"])


@router.post(
    "/",
    response_model=CourseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Opprett et nytt kurs",
)
def create_course(
    course_in: CourseCreate,
    db: Session = Depends(get_db),
):
    # Sjekker om kurset allerede eksisterer
    existing_course = db.scalar(
        select(CourseModel).where(CourseModel.course_name == course_in.course_name)
    )
    if existing_course:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Et kurs med dette navnet eksisterer allerede",
        )

    db_course = CourseModel(**course_in.model_dump())
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


@router.get("/search", response_model=list[CourseResponse])
def search_courses(
    query: str = Query(..., min_length=2, description="Søkeord (minst 2 tegn)"),
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=50, description="Maks antall treff som returneres"),
) -> list[CourseModel]:
    search_term = f"%{query.strip()}%"

    stmt = (
        select(CourseModel)
        .where(
            or_(
                CourseModel.course_name.ilike(search_term),
                CourseModel.course_provider.ilike(search_term),
            )
        )
        .order_by(CourseModel.course_name)
        .limit(limit)
    )

    return list(db.scalars(stmt).all())


@router.get("/{id}", response_model=CourseResponse)
def get_course(id: int, db: Session = Depends(get_db)):
    course = db.get(CourseModel, id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kurs med ID {id} ble ikke funnet",
        )
    return course


@router.get("/", response_model=list[CourseResponse])
def get_all_courses(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0, description="Antall rader å hoppe over"),
    limit: int = Query(50, ge=1, le=100, description="Maks antall rader (maks 100)"),
):
    stmt = select(CourseModel).offset(skip).limit(limit)
    return db.scalars(stmt).all()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_course(id: int, db: Session = Depends(get_db)):
    course = db.get(CourseModel, id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kurs med ID {id} ble ikke funnet",
        )
    db.delete(course)
    db.commit()


# Legge til person på et kurs
@router.post(
    "/{course_id}/members/{person_id}",
    response_model=CourseMemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Legg til en person på et kurs",
)
def add_person_to_course(
    course_id: int,
    person_id: int,
    course_date: date | None = Query(
        None, description="Dato for gjennomføring/påmelding (standard: i dag)"
    ),
    db: Session = Depends(get_db),
):
    # 1. Sjekk at kurs og person finnes
    if not db.get(CourseModel, course_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kurs med ID {course_id} finnes ikke",
        )

    if not db.get(PersonModel, person_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {person_id} finnes ikke",
        )

    # 2. Sjekk om personen allerede er meldt på kurset
    if db.get(PersonCourseModel, (person_id, course_id)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Personen er allerede meldt på dette kurset",
        )

    # 3. Opprett påmelding med oppgitt dato eller dagens dato
    enrollment = PersonCourseModel(
        person_id=person_id,
        course_id=course_id,
        course_date=course_date or date.today(),
    )
    db.add(enrollment)
    db.commit()
    db.refresh(enrollment)
    return enrollment


@router.get(
    "/{course_id}/members",
    response_model=list[person_response],
    summary="Hent alle personer på et spesifikt kurs",
)
def get_course_members(
    course_id: int,
    db: Session = Depends(get_db),
):
    course = db.get(CourseModel, course_id)
    if not course:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Kurs med ID {course_id} ble ikke funnet",
        )

    # JOIN mellom Person og koblingstabellen PersonCourse
    stmt = (
        select(PersonModel)
        .join(PersonCourseModel, PersonModel.id == PersonCourseModel.person_id)
        .where(PersonCourseModel.course_id == course_id)
    )

    return db.scalars(stmt).all()


@router.delete(
    "/{course_id}/members/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Fjern en person fra et kurs",
)
def remove_person_from_course(
    course_id: int,
    person_id: int,
    db: Session = Depends(get_db),
):
    enrollment = db.get(PersonCourseModel, (person_id, course_id))
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personen er ikke påmeldt dette kurset",
        )
    db.delete(enrollment)
    db.commit()
