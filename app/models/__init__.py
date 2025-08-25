"""
Models Brick

PUBLIC CONTRACT:
- Base: SQLAlchemy declarative base
- SessionLocal: Database session factory
- get_db(): Database session dependency
- User, Experiment, etc.: Database model classes

RESPONSIBILITIES:
- Database model definitions
- Database session management
- Data validation and serialization
- Database relationships and constraints
"""

from .database import Base
from .database import SessionLocal
from .database import get_db
from .user import User

__all__ = ["Base", "SessionLocal", "get_db", "User"]
