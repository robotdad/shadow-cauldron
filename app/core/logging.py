"""
Logging configuration for Shadow Cauldron.

Sets up structured logging using structlog.
"""

import sys
from typing import Any

import structlog


def setup_logging() -> None:
    """
    Configure structured logging for the application.

    Uses structlog for consistent, structured log output that's
    both human-readable in development and machine-parsable in production.
    """

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if sys.stderr.isatty() else structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(20),  # INFO level
        logger_factory=structlog.WriteLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> Any:
    """Get a logger instance for a module."""
    return structlog.get_logger(name)
