from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from personaldatabase.api.deps import get_current_person
from personaldatabase.core.security import create_access_token, verify_password
from personaldatabase.database.session import get_db
from personaldatabase.models.person_model import PersonModel
from personaldatabase.schemas.person import person_response

router = APIRouter(prefix="/auth", tags=["Auth"])


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=Token, summary="Logg inn med e-post og passord")
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    email = form_data.username.strip().lower()
    person = db.scalar(select(PersonModel).where(PersonModel.email == email))

    if not person or not person.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Feil e-postadresse eller passord",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not verify_password(form_data.password, person.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Feil e-postadresse eller passord",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not person.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Brukerkontoen er deaktivert",
        )

    access_token = create_access_token(subject=person.id)
    return Token(access_token=access_token)


@router.get("/me", response_model=person_response, summary="Hent innlogget person")
def read_current_person(
    current_person: PersonModel = Depends(get_current_person),
):
    return current_person
