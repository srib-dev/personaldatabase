import asyncio
from contextlib import asynccontextmanager, suppress
from fastapi import FastAPI
from personaldatabase.crud.person import deactivate_expired_persons
from personaldatabase.database.session import SessionLocal


async def periodic_semester_check():
    while True:
        with SessionLocal() as db:
            deactivate_expired_persons(db)
        await asyncio.sleep(86400)  # Sjekk en gang i døgnet (24 timer)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Kjører ved oppstart
    task = asyncio.create_task(periodic_semester_check())
    yield
    # Rydd opp når serveren avsluttes
    task.cancel()
    with suppress(asyncio.CancelledError):
        await task
