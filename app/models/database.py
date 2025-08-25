"""
Database configuration and session management.

Handles SQLAlchemy setup, connection management, and session lifecycle.
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.orm import sessionmaker

from ..config import settings

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    echo=settings.DB_ECHO,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create declarative base for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Database session dependency.

    This is the standard dependency that other bricks use
    to get database sessions in their endpoints.

    Yields:
        Database session that's automatically closed after use
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
