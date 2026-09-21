from fastapi import APIRouter
from personaldatabase.api.v1.users import router as users_router
from personaldatabase.api.v1.persons import router as persons_router

api_router = APIRouter()
api_router.include_router(users_router)
api_router.include_router(persons_router)
