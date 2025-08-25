"""
Middleware configuration for Shadow Cauldron.

Handles request/response processing, logging, and error handling.
"""

import time
import uuid
from collections.abc import Callable

import structlog
from fastapi import FastAPI
from fastapi import Request
from fastapi import Response
from fastapi.responses import JSONResponse

logger = structlog.get_logger(__name__)


def setup_middleware(app: FastAPI) -> None:
    """
    Configure middleware for the FastAPI application.

    Adds request logging, correlation IDs, and error handling.
    """

    @app.middleware("http")
    async def request_logging_middleware(request: Request, call_next: Callable) -> Response:
        """
        Log requests and responses with correlation IDs.

        Adds structured logging for all HTTP requests including timing,
        status codes, and correlation IDs for tracing.
        """
        # Generate correlation ID for request tracing
        correlation_id = str(uuid.uuid4())

        # Add correlation ID to request state
        request.state.correlation_id = correlation_id

        # Start timer
        start_time = time.time()

        # Log incoming request
        logger.info(
            "Request started",
            correlation_id=correlation_id,
            method=request.method,
            url=str(request.url),
            client_ip=request.client.host if request.client else None,
        )

        try:
            # Process request
            response = await call_next(request)

            # Calculate processing time
            process_time = time.time() - start_time

            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id

            # Log response
            logger.info(
                "Request completed",
                correlation_id=correlation_id,
                status_code=response.status_code,
                process_time=round(process_time * 1000, 2),  # milliseconds
            )

            return response

        except Exception as exc:
            # Calculate processing time for failed requests
            process_time = time.time() - start_time

            # Log error
            logger.error(
                "Request failed",
                correlation_id=correlation_id,
                error=str(exc),
                process_time=round(process_time * 1000, 2),
                exc_info=True,
            )

            # Return generic error response
            return JSONResponse(
                status_code=500,
                content={"error": "Internal server error", "correlation_id": correlation_id},
                headers={"X-Correlation-ID": correlation_id},
            )
