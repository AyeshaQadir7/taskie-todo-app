"""
Authentication Error Handlers

This module provides standardized error handlers for authentication
and authorization failures (401 Unauthorized, 403 Forbidden).

Spec: 002-authentication-jwt
Created: 2026-01-09
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
import logging


# Configure logging
logger = logging.getLogger(__name__)


async def unauthorized_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle 401 Unauthorized errors with standardized response format.

    This handler is called when JWT validation fails or authentication is required.

    Args:
        request: FastAPI request object
        exc: HTTP exception with 401 status code

    Returns:
        JSONResponse: Standardized 401 error response
    """
    logger.warning(
        f"401 Unauthorized: {request.method} {request.url.path} - {exc.detail}"
    )

    # Extract detail and message from exception
    if isinstance(exc.detail, dict):
        detail = exc.detail.get("detail", "Unauthorized")
        message = exc.detail.get("message", "Authentication required")
    else:
        detail = "Unauthorized"
        message = str(exc.detail)

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": detail,
            "message": message
        },
        headers={"WWW-Authenticate": "Bearer"}  # RFC 6750 requirement
    )


async def forbidden_error_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle 403 Forbidden errors with standardized response format.

    This handler is called when a user attempts to access resources they don't own.

    Args:
        request: FastAPI request object
        exc: HTTP exception with 403 status code

    Returns:
        JSONResponse: Standardized 403 error response
    """
    logger.warning(
        f"403 Forbidden: {request.method} {request.url.path} - {exc.detail}"
    )

    # Extract detail and message from exception
    if isinstance(exc.detail, dict):
        detail = exc.detail.get("detail", "Forbidden")
        message = exc.detail.get("message", "Access denied")
    else:
        detail = "Forbidden"
        message = str(exc.detail)

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "detail": detail,
            "message": message
        }
    )


def register_error_handlers(app):
    """
    Register authentication error handlers with FastAPI app.

    This function should be called during app initialization to set up
    standardized error handling for authentication failures.

    Usage:
        from fastapi import FastAPI
        from auth.error_handlers import register_error_handlers

        app = FastAPI()
        register_error_handlers(app)

    Args:
        app: FastAPI application instance
    """
    # Note: FastAPI automatically handles HTTPException responses,
    # so we don't need to add custom exception handlers here.
    # The error_handler functions above are for reference and can be used
    # if custom exception handling is needed.
    pass
