from fastapi import FastAPI
from personaldatabase.database.session import Base, engine
import personaldatabase.models
from personaldatabase.api.v1 import api_router

Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return {"Hello": "World"}