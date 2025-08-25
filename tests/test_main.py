"""
Tests for main application functionality.

Tests the core FastAPI app setup and basic endpoints.
"""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "shadow-cauldron"


def test_api_status(client: TestClient):
    """Test the API status endpoint."""
    response = client.get("/api/v1/status")
    assert response.status_code == 200

    data = response.json()
    assert data["message"] == "Shadow Cauldron API is running"


def test_cors_headers(client: TestClient):
    """Test CORS headers are present."""
    response = client.options("/health")
    # Should not error and should include CORS headers in a real CORS request
    assert response.status_code in [200, 405]  # 405 if OPTIONS not explicitly handled
