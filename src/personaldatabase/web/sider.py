from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from personaldatabase.database.session import get_db
from personaldatabase.models import (
    PersonCourseModel,
    PersonGroupModel,
    PersonModel,
    PersonVervModel,
)

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

router = APIRouter()

# TODO: erstatt med innlogget bruker når innlogging er på plass
INNLOGGET_PERSON_ID = 1


def vis_person(request: Request, db: Session, id: int, kan_redigere: bool):
    person = db.scalar(
        select(PersonModel)
        .where(PersonModel.id == id)
        .options(
            selectinload(PersonModel.verv).selectinload(PersonVervModel.verv),
            selectinload(PersonModel.groups).selectinload(PersonGroupModel.group),
            selectinload(PersonModel.courses).selectinload(PersonCourseModel.course),
        )
    )
    if not person:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Person med ID {id} ble ikke funnet",
        )
    return templates.TemplateResponse(request, "profil/vis.html", {
        "person": person,
        "kan_redigere": kan_redigere,
    })


@router.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard/index.html")


@router.get("/statistikk")
def statistikk(request: Request):
    return templates.TemplateResponse(request, "statistikk/index.html")


@router.get("/min-profil")
def min_profil(request: Request, db: Session = Depends(get_db)):
    # TODO: sett kan_redigere ut fra tilgangen til innlogget bruker
    return vis_person(request, db, INNLOGGET_PERSON_ID, kan_redigere=True)


@router.get("/profil/ny")
def ny_profil(request: Request):
    return templates.TemplateResponse(request, "profil/ny.html")


@router.get("/profil/{id}")
def vis_profil(request: Request, id: int, db: Session = Depends(get_db)):
    # TODO: sett kan_redigere ut fra tilgangen til innlogget bruker
    return vis_person(request, db, id, kan_redigere=True)


@router.get("/grupper")
def grupper(request: Request):
    return templates.TemplateResponse(request, "grupper/liste.html")


@router.get("/grupper/{id}")
def vis_gruppe(request: Request, id: int):
    return templates.TemplateResponse(request, "grupper/vis.html")


@router.get("/kurs")
def kurs(request: Request):
    return templates.TemplateResponse(request, "kurs/liste.html")


@router.get("/godkjenning")
def godkjenning(request: Request):
    return templates.TemplateResponse(request, "godkjenning/index.html")


@router.get("/admin")
def admin(request: Request):
    return templates.TemplateResponse(request, "admin/index.html", {
        "er_superadmin": True,
        "admin_brukere": [],
        "grupper": [],
    })
