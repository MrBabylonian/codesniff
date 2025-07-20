from fastapi import FastAPI

from .database.engine import Base, engine
from .database import models

# Create all tables in the database
models.User.metadata.create_all(bind=engine)
models.GithubRepository.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)

app: FastAPI = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World!"}
