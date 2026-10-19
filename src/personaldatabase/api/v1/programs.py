from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from personaldatabase.database.session import get_db
from personaldatabase.models.group_model import GroupModel
from personaldatabase.models.person_model import PersonModel
from personaldatabase.models.person_program_model import PersonProgramModel
from personaldatabase.models.program_model import ProgramModel
from personaldatabase.schemas.person import person_response
from personaldatabase.schemas.person_program import ProgramMemberResponse
from personaldatabase.schemas.program import ProgramCreate, ProgramResponse

router = APIRouter(prefix="/programs", tags=["Programs"])


@router.post(
    "/",
    response_model=ProgramResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Opprett et nytt program",
)
def create_program(
    program_in: ProgramCreate,
    db: Session = Depends(get_db),
):
    if not db.get(GroupModel, program_in.group_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Gruppe med ID {program_in.group_id} finnes ikke",
        )

    # Sjekker om gruppen allerede har et program med samme navn
    existing_program = db.scalar(
        select(ProgramModel).where(
            ProgramModel.program_name == program_in.program_name,
            ProgramModel.group_id == program_in.group_id,
        )
    )
    if existing_program:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Gruppen har allerede et program med dette navnet",
        )

    db_program = ProgramModel(**program_in.model_dump())
    db.add(db_program)
    db.commit()
    db.refresh(db_program)
    return db_program


@router.get("/search", response_model=list[ProgramResponse])
def search_programs(
    query: str = Query(..., min_length=2, description="Søkeord (minst 2 tegn)"),
    db: Session = Depends(get_db),
    limit: int = Query(20, ge=1, le=50, description="Maks antall treff som returneres"),
) -> list[ProgramModel]:
    search_term = f"%{query.strip()}%"

    stmt = (
        select(ProgramModel)
        .where(ProgramModel.program_name.ilike(search_term))
        .order_by(ProgramModel.program_name)
        .limit(limit)
    )

    return list(db.scalars(stmt).all())


@router.get("/{id}", response_model=ProgramResponse)
def get_program(id: int, db: Session = Depends(get_db)):
    program = db.get(ProgramModel, id)
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program med ID {id} ble ikke funnet",
        )
    return program


@router.get("/", response_model=list[ProgramResponse])
def get_all_programs(
    db: Session = Depends(get_db),
    group_id: int | None = Query(None, description="Vis bare programmer for denne gruppen"),
    skip: int = Query(0, ge=0, description="Antall rader å hoppe over"),
    limit: int = Query(50, ge=1, le=100, description="Maks antall rader (maks 100)"),
):
    stmt = select(ProgramModel)
    if group_id is not None:
        stmt = stmt.where(ProgramModel.group_id == group_id)
    stmt = stmt.offset(skip).limit(limit)
    return db.scalars(stmt).all()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_program(id: int, db: Session = Depends(get_db)):
    program = db.get(ProgramModel, id)
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program med ID {id} ble ikke funnet",
        )
    db.delete(program)
    db.commit()


# Legge til person i et program
@router.post(
    "/{program_id}/members/{person_id}",
    response_model=ProgramMemberResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Legg til en person i et program med en rolle",
)
def add_person_to_program(
    program_id: int,
    person_id: int,
    program_role: str = Query(..., min_length=1, description="Rollen personen har i programmet"),
    db: Session = Depends(get_db),
):
    # 1. Sjekk at program og person finnes
    if not db.get(ProgramModel, program_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program med ID {program_id} finnes ikke",
        )

    if not db.get(PersonModel, person_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {person_id} finnes ikke",
        )

    # 2. Sjekk om personen allerede er med i programmet
    if db.get(PersonProgramModel, (person_id, program_id)):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Personen er allerede med i dette programmet",
        )

    # 3. Opprett kobling med rolle
    membership = PersonProgramModel(
        person_id=person_id,
        program_id=program_id,
        program_role=program_role,
    )
    db.add(membership)
    db.commit()
    db.refresh(membership)
    return membership


@router.get(
    "/{program_id}/members",
    response_model=list[person_response],
    summary="Hent alle personer i et spesifikt program",
)
def get_program_members(
    program_id: int,
    db: Session = Depends(get_db),
):
    program = db.get(ProgramModel, program_id)
    if not program:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Program med ID {program_id} ble ikke funnet",
        )

    # JOIN mellom Person og koblingstabellen PersonProgram
    stmt = (
        select(PersonModel)
        .join(PersonProgramModel, PersonModel.id == PersonProgramModel.person_id)
        .where(PersonProgramModel.program_id == program_id)
    )

    return db.scalars(stmt).all()


@router.get(
    "/{program_id}/members/{person_id}",
    response_model=ProgramMemberResponse,
    summary="Hent rollen en person har i et program",
)
def get_person_program_role(
    program_id: int,
    person_id: int,
    db: Session = Depends(get_db),
):
    membership = db.get(PersonProgramModel, (person_id, program_id))
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personen er ikke med i dette programmet",
        )
    return membership


@router.delete(
    "/{program_id}/members/{person_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Fjern en person fra et program",
)
def remove_person_from_program(
    program_id: int,
    person_id: int,
    db: Session = Depends(get_db),
):
    membership = db.get(PersonProgramModel, (person_id, program_id))
    if not membership:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Personen er ikke med i dette programmet",
        )
    db.delete(membership)
    db.commit()
