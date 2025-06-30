import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")
engine = create_engine(DATABASE_URL)


def get_session() -> Generator:
    with Session(engine) as session:
        yield session
