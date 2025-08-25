"""
User model for Shadow Cauldron.

Defines the user entity with authentication and profile information.
"""

import uuid
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.types import String as SQLString
from sqlalchemy.types import TypeDecorator

from .database import Base


class UUIDType(TypeDecorator):
    """UUID type that works with SQLite and PostgreSQL."""

    impl = SQLString
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return str(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return uuid.UUID(value)
        return value


class User(Base):
    """
    User model for authentication and profile management.

    This is a basic user model that can be extended as needed.
    """

    __tablename__ = "users"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    # Profile fields
    full_name = Column(String(255))
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username='{self.username}')>"
