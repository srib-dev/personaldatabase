from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from personaldatabase.database.session import get_db
from personaldatabase.models.award_model import AwardModel
from personaldatabase.models.award_win_model import AwardWinModel
from personaldatabase.models.award_win_person_model import AwardWinPersonModel
from personaldatabase.models.person_model import PersonModel
from personaldatabase.models.person_program_model import PersonProgramModel
from personaldatabase.models.program_model import ProgramModel
from personaldatabase.schemas.award import (
    AwardCreate,
    AwardResponse,
    AwardUpdate,
    AwardWinCreate,
    AwardWinPersonResponse,
    AwardWinResponse,
)
from personaldatabase.schemas.person import person_response
from personaldatabase.schemas.program import ProgramResponse

router = APIRouter(prefix="/awards", tags=["Awards"])


def _award_win_query():
    return select(AwardWinModel).options(
        selectinload(AwardWinModel.award),
        selectinload(AwardWinModel.program),
        selectinload(AwardWinModel.persons).selectinload(AwardWinPersonModel.person),
    )


@router.post(
    "/",
    response_model=AwardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Opprett en ny priskategori",
)
def create_award(
    award_in: AwardCreate,
    db: Session = Depends(get_db),
):
    existing_award = db.scalar(
        select(AwardModel).where(AwardModel.award_name == award_in.award_name)
    )
    if existing_award:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="En pris med dette navnet eksisterer allerede",
        )

    db_award = AwardModel(**award_in.model_dump())
    db.add(db_award)
    db.commit()
    db.refresh(db_award)
    return db_award


@router.get(
    "/search",
    response_model=list[AwardResponse],
    summary="Søk etter priskategorier",
)
def search_awards(
    query: str = Query(..., min_length=2, description="Søkeord (minst 2 tegn)"),
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=50, description="Maks antall treff som returneres"),
) -> list[AwardModel]:
    search_term = f"%{query.strip()}%"

    stmt = (
        select(AwardModel)
        .where(
            or_(
                AwardModel.award_name.ilike(search_term),
                AwardModel.description.ilike(search_term),
            )
        )
        .order_by(AwardModel.award_name)
        .limit(limit)
    )

    return list(db.scalars(stmt).all())


@router.get(
    "/",
    response_model=list[AwardResponse],
    summary="Hent alle priskategorier",
)
def get_all_awards(
    db: Session = Depends(get_db),
    is_program_award: bool | None = Query(
        None, description="Filtrer på om prisen er en programpris eller personpris"
    ),
    skip: int = Query(0, ge=0, description="Antall rader å hoppe over"),
    limit: int = Query(50, ge=1, le=100, description="Maks antall rader (maks 100)"),
):
    stmt = select(AwardModel)
    if is_program_award is not None:
        stmt = stmt.where(AwardModel.is_program_award == is_program_award)
    stmt = stmt.order_by(AwardModel.award_name).offset(skip).limit(limit)
    return db.scalars(stmt).all()


@router.get(
    "/wins",
    response_model=list[AwardWinResponse],
    summary="Hent prisutdelinger på tvers av priser",
)
def get_all_award_wins(
    db: Session = Depends(get_db),
    award_id: int | None = Query(None, description="Filtrer på priskategori-ID"),
    program_id: int | None = Query(None, description="Filtrer på program-ID"),
    person_id: int | None = Query(None, description="Filtrer på vinner-person-ID"),
    semester: str | None = Query(None, description="Filtrer på semester (f.eks. H2025)"),
    skip: int = Query(0, ge=0, description="Antall rader å hoppe over"),
    limit: int = Query(50, ge=1, le=100, description="Maks antall rader (maks 100)"),
):
    stmt = _award_win_query()
    if award_id is not None:
        stmt = stmt.where(AwardWinModel.award_id == award_id)
    if program_id is not None:
        stmt = stmt.where(AwardWinModel.program_id == program_id)
    if person_id is not None:
        stmt = stmt.where(
            AwardWinModel.persons.any(AwardWinPersonModel.person_id == person_id)
        )
    if semester is not None:
        stmt = stmt.where(AwardWinModel.semester.ilike(semester.strip()))

    stmt = stmt.order_by(AwardWinModel.id.desc()).offset(skip).limit(limit)
    return db.scalars(stmt).all()


@router.get(
    "/wins/{win_id}",
    response_model=AwardWinResponse,
    summary="Hent en spesifikk prisutdeling",
)
def get_award_win(win_id: int, db: Session = Depends(get_db)):
    stmt = _award_win_query().where(AwardWinModel.id == win_id)
    award_win = db.scalar(stmt)
    if not award_win:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prisutdeling med ID {win_id} ble ikke funnet",
        )
    return award_win


@router.delete(
    "/wins/{win_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Slett en prisutdeling",
)
def delete_award_win(win_id: int, db: Session = Depends(get_db)):
    award_win = db.get(AwardWinModel, win_id)
    if not award_win:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prisutdeling med ID {win_id} ble ikke funnet",
        )
    db.delete(award_win)
    db.commit()


@router.post(
    "/wins/{win_id}/persons/{person_id}",
    response_model=AwardWinPersonResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Legg til en person på en prisutdeling",
)
def add_person_to_award_win(
    win_id: int,
    person_id: int,
    db: Session = Depends(get_db),
):
    if not db.get(AwardWinModel, win_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Prisutdeling med ID {win_id} finnes ikke",
        )

    if not db.get(PersonModel, person_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {person_id} finnes ikke",
        )

    if db.get(AwardWinPersonModel, (win_id, person_id)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Personen er allerede registrert på denne prisutdelingen",
        )

    link = AwardWinPersonModel(award_win_id=win_id, person_id=person_id)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


@router.delete(
    "/wins/{win_id}/persons/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Fjern en person fra en prisutdeling",
)
def remove_person_from_award_win(
    win_id: int,
    person_id: int,
    db: Session = Depends(get_db),
):
    link = db.get(AwardWinPersonModel, (win_id, person_id))
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personen er ikke registrert på denne prisutdelingen",
        )
    db.delete(link)
    db.commit()


@router.get(
    "/{id}",
    response_model=AwardResponse,
    summary="Hent en priskategori med ID",
)
def get_award(id: int, db: Session = Depends(get_db)):
    award = db.get(AwardModel, id)
    if not award:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pris med ID {id} ble ikke funnet",
        )
    return award


@router.patch(
    "/{id}",
    response_model=AwardResponse,
    summary="Oppdater en priskategori",
)
def update_award(
    id: int,
    award_in: AwardUpdate,
    db: Session = Depends(get_db),
):
    award = db.get(AwardModel, id)
    if not award:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pris med ID {id} ble ikke funnet",
        )

    update_data = award_in.model_dump(exclude_unset=True)
    if "award_name" in update_data and update_data["award_name"] != award.award_name:
        existing = db.scalar(
            select(AwardModel).where(
                AwardModel.award_name == update_data["award_name"],
                AwardModel.id != id,
            )
        )
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="En pris med dette navnet eksisterer allerede",
            )

    for field, value in update_data.items():
        setattr(award, field, value)

    db.commit()
    db.refresh(award)
    return award


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Slett en priskategori",
)
def delete_award(id: int, db: Session = Depends(get_db)):
    award = db.get(AwardModel, id)
    if not award:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pris med ID {id} ble ikke funnet",
        )
    db.delete(award)
    db.commit()


@router.post(
    "/{award_id}/wins",
    response_model=AwardWinResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Del ut en pris et gitt semester",
)
def create_award_win(
    award_id: int,
    win_in: AwardWinCreate,
    db: Session = Depends(get_db),
):
    """
    Registrerer en ny utdeling av en pris for et gitt semester:
    - Når et program vinner (`program_id` satt og `person_ids` utelatt, eller `copy_program_members=True`):
      Kopierer automatisk alle medlemmer av programmet fra `person_programs` inn i `award_win_persons`.
    - Når en enkeltperson vinner (`person_ids` oppgitt):
      Knytter de oppgitte personene i `award_win_persons` (med `program_id` satt til NULL eller programmet det gjaldt).
    """
    award = db.get(AwardModel, award_id)
    if not award:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pris med ID {award_id} finnes ikke",
        )

    if win_in.program_id is not None:
        program = db.get(ProgramModel, win_in.program_id)
        if not program:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Program med ID {win_in.program_id} finnes ikke",
            )

    if win_in.program_id is None and not win_in.person_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Du må oppgi enten program_id eller minst én person i person_ids",
        )

    winner_person_ids: set[int] = set()

    # Valider eventuelle eksplisitt oppgitte person_ids
    if win_in.person_ids:
        unique_person_ids = set(win_in.person_ids)
        existing_person_ids = set(
            db.scalars(
                select(PersonModel.id).where(PersonModel.id.in_(unique_person_ids))
            ).all()
        )
        missing_ids = unique_person_ids - existing_person_ids
        if missing_ids:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Følgende person-IDer finnes ikke: {sorted(missing_ids)}",
            )
        winner_person_ids.update(existing_person_ids)

    # Kopier programmedlemmer fra person_programs når et program vinner
    should_copy_program_members = (
        win_in.copy_program_members
        if win_in.copy_program_members is not None
        else (win_in.program_id is not None and not win_in.person_ids)
    )
    if win_in.program_id is not None and should_copy_program_members:
        program_member_ids = db.scalars(
            select(PersonProgramModel.person_id).where(
                PersonProgramModel.program_id == win_in.program_id
            )
        ).all()
        winner_person_ids.update(program_member_ids)

    db_win = AwardWinModel(
        award_id=award_id,
        semester=win_in.semester.strip(),
        program_id=win_in.program_id,
        note=win_in.note,
    )
    db.add(db_win)
    db.flush()

    for pid in sorted(winner_person_ids):
        db.add(AwardWinPersonModel(award_win_id=db_win.id, person_id=pid))

    db.commit()

    stmt = _award_win_query().where(AwardWinModel.id == db_win.id)
    return db.scalar(stmt)


@router.get(
    "/{award_id}/wins",
    response_model=list[AwardWinResponse],
    summary="Hent alle utdelinger av en spesifikk pris gjennom tidene",
)
def get_award_wins_for_award(
    award_id: int,
    semester: str | None = Query(None, description="Filtrer på semester (f.eks. H2025)"),
    db: Session = Depends(get_db),
):
    if not db.get(AwardModel, award_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pris med ID {award_id} ble ikke funnet",
        )

    stmt = _award_win_query().where(AwardWinModel.award_id == award_id)
    if semester is not None:
        stmt = stmt.where(AwardWinModel.semester.ilike(semester.strip()))
    stmt = stmt.order_by(AwardWinModel.id.desc())
    return db.scalars(stmt).all()


@router.get(
    "/{award_id}/persons",
    response_model=list[person_response],
    summary="Hent alle personer som har vunnet en spesifikk pris gjennom tidene",
)
def get_award_winning_persons(
    award_id: int,
    db: Session = Depends(get_db),
):
    if not db.get(AwardModel, award_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pris med ID {award_id} ble ikke funnet",
        )

    stmt = (
        select(PersonModel)
        .join(AwardWinPersonModel, PersonModel.id == AwardWinPersonModel.person_id)
        .join(AwardWinModel, AwardWinPersonModel.award_win_id == AwardWinModel.id)
        .where(AwardWinModel.award_id == award_id)
        .distinct()
        .order_by(PersonModel.last_name, PersonModel.first_name)
    )
    return db.scalars(stmt).all()


@router.get(
    "/{award_id}/programs",
    response_model=list[ProgramResponse],
    summary="Hent alle programmer som har vunnet en spesifikk pris gjennom tidene",
)
def get_award_winning_programs(
    award_id: int,
    db: Session = Depends(get_db),
):
    if not db.get(AwardModel, award_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Pris med ID {award_id} ble ikke funnet",
        )

    stmt = (
        select(ProgramModel)
        .join(AwardWinModel, ProgramModel.id == AwardWinModel.program_id)
        .where(AwardWinModel.award_id == award_id)
        .distinct()
        .order_by(ProgramModel.program_name)
    )
    return db.scalars(stmt).all()
