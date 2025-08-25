"""
Core Brick

PUBLIC CONTRACT:
- setup_logging(): Initialize structured logging
- setup_middleware(app): Configure FastAPI middleware
- get_current_user(): Authentication dependency
- AuthenticatedUser: User model for authenticated requests

RESPONSIBILITIES:
- Authentication and authorization
- Request/response middleware
- Structured logging setup
- Security utilities
"""

from .auth import AuthenticatedUser
from .auth import get_current_user
from .logging import setup_logging
from .middleware import setup_middleware

__all__ = [
    "setup_logging",
    "setup_middleware",
    "get_current_user",
    "AuthenticatedUser",
]
