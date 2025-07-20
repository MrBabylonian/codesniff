import os

from dotenv import load_dotenv
from sqlalchemy import Engine, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")
if not POSTGRES_USER or not POSTGRES_PASSWORD or not POSTGRES_DB:
    raise ValueError(
        "Environment variables for PostgreSQL are not set properly.")
POSTGRES_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost/{POSTGRES_DB}"

# Creates the engine
engine: Engine = create_engine(POSTGRES_URL, echo=True)

# SessionLocal is a session factory function that creates new Session objects
# when called, which handle database transactions.
SessionLocal: sessionmaker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()
