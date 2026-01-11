"""
Database configuration and managing of the sessions
Based on: TodoApp/database.py
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from src.data.config.settings import get_settings

settings = get_settings()

# Create engine
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(settings.DATABASE_URL)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


def get_db():
    """
    Dependency that provides database session
    Ensures session is closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()