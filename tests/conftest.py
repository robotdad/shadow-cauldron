"""
Pytest configuration and shared fixtures for Shadow Cauldron tests.

Provides common test fixtures that can be used across all test modules.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.models.database import Base
from app.models.database import get_db


@pytest.fixture
def test_db():
    """Create a test database."""
    # Use in-memory SQLite for tests
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestingSessionLocal
    app.dependency_overrides.clear()


@pytest.fixture
def client(test_db):
    """Create a test client."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_user():
    """Sample user data for tests."""
    return {"username": "testuser", "email": "test@example.com", "password": "testpassword123"}
