import asyncio
from contextlib import asynccontextmanager, suppress
from fastapi import FastAPI
from personaldatabase.crud.person import deactivate_expired_persons
from personaldatabase.database.init_db import init_db
from personaldatabase.database.session import Base, SessionLocal, engine
import personaldatabase.models
from personaldatabase.api.v1 import api_router

Base.metadata.create_all(bind=engine)
init_db()


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


app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"Hello": "World"}