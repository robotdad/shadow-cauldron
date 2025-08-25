"""
Authentication and authorization for Shadow Cauldron.

Handles JWT tokens, user authentication, and authorization dependencies.
"""

from datetime import datetime
from datetime import timedelta

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from jose import JWTError
from jose import jwt
from pydantic import BaseModel

from ..config import settings

security = HTTPBearer()


class AuthenticatedUser(BaseModel):
    """Model for authenticated user data."""

    user_id: str
    username: str
    email: str | None = None
    is_admin: bool = False


def create_access_token(data: dict) -> str:
    """
    Create a JWT access token.

    Args:
        data: Dictionary of claims to include in token

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")


def verify_token(token: str) -> dict:
    """
    Verify and decode a JWT token.

    Args:
        token: JWT token string

    Returns:
        Decoded token payload

    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> AuthenticatedUser:
    """
    Dependency to get the current authenticated user.

    This is the main authentication dependency that other bricks
    can use to protect endpoints and get user information.

    Returns:
        AuthenticatedUser model with user data

    Raises:
        HTTPException: If authentication fails
    """
    payload = verify_token(credentials.credentials)

    # Extract user data from token
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    # In a real implementation, you might fetch user data from database
    # For now, we'll use the data from the token
    return AuthenticatedUser(
        user_id=user_id,
        username=payload.get("username", "unknown"),
        email=payload.get("email"),
        is_admin=payload.get("is_admin", False),
    )
