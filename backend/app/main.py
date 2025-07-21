import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from pyngrok import ngrok

from .database import models
from .database.engine import Base, engine

load_dotenv()

NGROK_AUTH_TOKEN = os.getenv("NGROK_AUTH_TOKEN")

# Create all tables in the database
models.User.metadata.create_all(bind=engine)
models.GithubRepository.metadata.create_all(bind=engine)
Base.metadata.create_all(bind=engine)


def start_ngrok():
    ngrok.set_auth_token(NGROK_AUTH_TOKEN)
    public_url = ngrok.connect(
        8000, url="welcome-killdeer-jointly.ngrok-free.app", bind_tls=True)
    print(f"Public URL: {public_url}")
    print("Ngrok tunnel established. You can now access your backend at the public URL.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    public_url = start_ngrok()
    yield
    ngrok.disconnect(public_url)
    ngrok.kill()

app: FastAPI = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.get("/getme")
async def get_me():
    return {"message": "This is a test endpoint to verify the backend is running."}
