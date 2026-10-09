from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

router = APIRouter()


@router.get("/")
def dashboard(request: Request):
    return templates.TemplateResponse(request, "dashboard/index.html")


@router.get("/statistikk")
def statistikk(request: Request):
    return templates.TemplateResponse(request, "statistikk/index.html")


@router.get("/min-profil")
def min_profil(request: Request):
    return templates.TemplateResponse(request, "profil/vis.html")


@router.get("/profil/ny")
def ny_profil(request: Request):
    return templates.TemplateResponse(request, "profil/ny.html")


@router.get("/profil/{id}")
def vis_profil(request: Request, id: int):
    return templates.TemplateResponse(request, "profil/vis.html")


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
