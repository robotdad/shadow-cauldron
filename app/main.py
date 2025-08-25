"""
Shadow Cauldron - Main FastAPI Application

This is the entry point that assembles all the modular bricks.
Each brick provides its contract through well-defined interfaces.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router as api_router
from .config import settings
from .core import setup_logging
from .core import setup_middleware


def create_app() -> FastAPI:
    """
    Create the FastAPI application by assembling all bricks.

    This follows the "bricks and studs" philosophy:
    - Each import connects to a brick's public interface
    - Internal implementation details are hidden
    - Bricks can be regenerated independently
    """
    # Initialize structured logging
    setup_logging()

    # Create FastAPI app
    app = FastAPI(
        title="Shadow Cauldron",
        description="AI Experimentation Platform",
        version="0.1.0",
        docs_url="/docs" if settings.DEBUG else None,
        redoc_url="/redoc" if settings.DEBUG else None,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Setup additional middleware from core brick
    setup_middleware(app)

    # Include API routes from api brick
    app.include_router(api_router, prefix="/api/v1")

    return app


# Create the application instance
app = create_app()


@app.get("/health")
async def health_check():
    """Simple health check endpoint."""
    return {"status": "healthy", "service": "shadow-cauldron"}
