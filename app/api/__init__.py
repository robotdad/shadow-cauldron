"""
API Brick

PUBLIC CONTRACT:
- router: Main API router to include in FastAPI app

RESPONSIBILITIES:
- HTTP endpoint definitions
- Request/response models
- Route organization and grouping
- API versioning
"""

from .routes import router

__all__ = ["router"]
