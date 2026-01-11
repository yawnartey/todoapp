# transportation/api/dependencies/database.py
"""
Database dependency for FastAPI
Based on: TodoApp/database.py (get_db function)
"""

from typing import Generator
from sqlalchemy.orm import Session

from src.data.config.database import SessionLocal


def get_db() -> Generator[Session, None, None]:

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()