"""
API routes for Shadow Cauldron.

Organizes all HTTP endpoints into logical groups.
Each route group can be moved to separate files as they grow.
"""

from fastapi import APIRouter
from fastapi import Depends
from pydantic import BaseModel

from ..core import AuthenticatedUser
from ..core import get_current_user

# Create main API router
router = APIRouter()


class MessageResponse(BaseModel):
    """Standard response model for simple messages."""

    message: str


@router.get("/status", response_model=MessageResponse)
async def get_status():
    """Get API status - public endpoint."""
    return MessageResponse(message="Shadow Cauldron API is running")


@router.get("/protected", response_model=MessageResponse)
async def protected_endpoint(user: AuthenticatedUser = Depends(get_current_user)):
    """Example protected endpoint that requires authentication."""
    return MessageResponse(message=f"Hello {user.username}, you are authenticated!")


# Placeholder routes for future bricks
# These will be moved to separate router files as functionality is implemented


@router.get("/experiments", response_model=MessageResponse)
async def list_experiments(user: AuthenticatedUser = Depends(get_current_user)):
    """List experiments - placeholder for experiments brick."""
    return MessageResponse(message="Experiments functionality will be implemented")


@router.get("/providers", response_model=MessageResponse)
async def list_providers(user: AuthenticatedUser = Depends(get_current_user)):
    """List AI providers - placeholder for providers brick."""
    return MessageResponse(message="Providers functionality will be implemented")
