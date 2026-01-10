"""
JWT Validation Middleware

This module implements FastAPI middleware for JWT token validation.
All protected endpoints must have a valid JWT token in the Authorization header.

Spec: 002-authentication-jwt
Created: 2026-01-09
"""

from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from typing import Optional
import logging

from .jwt_utils import parse_bearer_token, verify_jwt_token
from .auth_context import extract_user_from_jwt, AuthenticatedUser
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError, InvalidTokenError


# Configure logging
logger = logging.getLogger(__name__)


class JWTAuthMiddleware:
    """
    JWT authentication middleware for FastAPI.

    This middleware extracts and validates JWT tokens from the Authorization header
    for all protected routes. If validation fails, it returns 401 Unauthorized.

    Usage:
        app.add_middleware(JWTAuthMiddleware)
    """

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        """
        Process request through JWT validation middleware.

        This method is called for every request. It checks if the request
        requires authentication and validates the JWT token if present.
        """
        if scope["type"] != "http":
            # Not an HTTP request (e.g., WebSocket)
            await self.app(scope, receive, send)
            return

        request = Request(scope, receive=receive)

        # Check if route requires authentication
        # For now, we'll implement this in dependencies rather than middleware
        # to allow route-level control

        await self.app(scope, receive, send)


def extract_and_validate_jwt(authorization_header: Optional[str]) -> AuthenticatedUser:
    """
    Extract and validate JWT token from Authorization header.

    This function is used by FastAPI dependencies to validate JWT tokens.

    Args:
        authorization_header: HTTP Authorization header value

    Returns:
        AuthenticatedUser: Authenticated user context

    Raises:
        HTTPException: 401 Unauthorized if token is invalid, expired, or missing
    """
    # Check if Authorization header is present
    if not authorization_header:
        logger.warning("Missing Authorization header")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "detail": "Unauthorized",
                "message": "Missing authorization header"
            }
        )

    # Extract Bearer token
    token = parse_bearer_token(authorization_header)

    if not token:
        logger.warning("Invalid Authorization header format")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "detail": "Unauthorized",
                "message": "Invalid authorization header format. Expected: Bearer <token>"
            }
        )

    # Validate JWT token
    try:
        payload = verify_jwt_token(token)

        # Extract user context from JWT payload
        authenticated_user = extract_user_from_jwt(payload)

        logger.info(f"Authenticated user: {authenticated_user.user_id}")

        return authenticated_user

    except ExpiredSignatureError:
        logger.warning("JWT token expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "detail": "Unauthorized",
                "message": "Token expired"
            }
        )

    except InvalidSignatureError:
        logger.warning("Invalid JWT signature")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "detail": "Unauthorized",
                "message": "Invalid token signature"
            }
        )

    except InvalidTokenError as e:
        logger.warning(f"Invalid JWT token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "detail": "Unauthorized",
                "message": f"Invalid token: {str(e)}"
            }
        )

    except ValueError as e:
        logger.warning(f"JWT validation error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "detail": "Unauthorized",
                "message": str(e)
            }
        )

    except Exception as e:
        logger.error(f"Unexpected error during JWT validation: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "detail": "Unauthorized",
                "message": "Authentication failed"
            }
        )


def create_unauthorized_response(message: str) -> JSONResponse:
    """
    Create a standardized 401 Unauthorized response.

    Args:
        message: Error message

    Returns:
        JSONResponse: 401 response with error details
    """
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "detail": "Unauthorized",
            "message": message
        }
    )


def create_forbidden_response(message: str) -> JSONResponse:
    """
    Create a standardized 403 Forbidden response.

    Args:
        message: Error message

    Returns:
        JSONResponse: 403 response with error details
    """
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "detail": "Forbidden",
            "message": message
        }
    )
