from fastapi import APIRouter
from personaldatabase.api.v1.auth import router as auth_router
from personaldatabase.api.v1.course import router as courses_router
from personaldatabase.api.v1.groups import router as groups_router
from personaldatabase.api.v1.persons import router as persons_router
from personaldatabase.api.v1.verv import router as verv_router

api_router = APIRouter()
api_router.include_router(auth_router)
api_router.include_router(groups_router)
api_router.include_router(persons_router)
api_router.include_router(courses_router)
api_router.include_router(verv_router)