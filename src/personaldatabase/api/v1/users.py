from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from personaldatabase.database.session import get_db
from personaldatabase.models.user_model import user_model
from personaldatabase.schemas.user import user_response

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{user_id}", response_model=user_response)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(user_model, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Bruker med ID {user_id} ble ikke funnet"
        )
    return user
