"""
JWT Dependency Injection for FastAPI

This module provides FastAPI dependency functions for JWT authentication
and authorization. These dependencies can be used to protect endpoints
and validate user ownership.

Spec: 002-authentication-jwt
Created: 2026-01-09
"""

from fastapi import Depends, Header, HTTPException, status
from typing import Optional
import logging

from .auth_context import AuthenticatedUser, verify_user_ownership
from .jwt_middleware import extract_and_validate_jwt


# Configure logging
logger = logging.getLogger(__name__)


def get_current_user(
    authorization: Optional[str] = Header(None)
) -> AuthenticatedUser:
    """
    FastAPI dependency to get the current authenticated user from JWT token.

    This dependency extracts and validates the JWT token from the Authorization
    header, then returns the authenticated user context.

    Usage:
        @app.get("/protected")
        def protected_endpoint(user: AuthenticatedUser = Depends(get_current_user)):
            return {"user_id": user.user_id}

    Args:
        authorization: Authorization header value (injected by FastAPI)

    Returns:
        AuthenticatedUser: Authenticated user context

    Raises:
        HTTPException: 401 Unauthorized if token is invalid or missing
    """
    return extract_and_validate_jwt(authorization)


def verify_path_user_id(
    user_id: str,
    current_user: AuthenticatedUser = Depends(get_current_user)
) -> AuthenticatedUser:
    """
    FastAPI dependency to verify that the authenticated user owns the resource.

    This dependency checks that the user_id from the JWT token matches the
    user_id in the route path. This enforces multi-user isolation.

    Usage:
        @app.get("/api/{user_id}/tasks")
        def get_tasks(
            user_id: str,
            user: AuthenticatedUser = Depends(verify_path_user_id)
        ):
            # user.user_id is guaranteed to equal user_id from path
            return {"tasks": [...]}

    Args:
        user_id: User ID from route path (injected by FastAPI)
        current_user: Authenticated user from JWT (injected by get_current_user)

    Returns:
        AuthenticatedUser: Authenticated user context (only if ownership verified)

    Raises:
        HTTPException: 403 Forbidden if user_id doesn't match JWT user_id
    """
    # Verify that JWT user_id matches route path user_id
    if not verify_user_ownership(current_user, user_id):
        logger.warning(
            f"Authorization failure: JWT user_id={current_user.user_id} "
            f"attempted to access user_id={user_id}"
        )

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "detail": "Forbidden",
                "message": "Access denied"
            }
        )

    logger.info(f"Authorization success: user_id={user_id}")

    return current_user


def require_auth(
    authorization: Optional[str] = Header(None)
) -> AuthenticatedUser:
    """
    Alias for get_current_user dependency.

    This provides a more readable name for endpoints that require authentication.

    Usage:
        @app.get("/protected")
        def protected_endpoint(user: AuthenticatedUser = Depends(require_auth)):
            return {"user_id": user.user_id}

    Args:
        authorization: Authorization header value (injected by FastAPI)

    Returns:
        AuthenticatedUser: Authenticated user context

    Raises:
        HTTPException: 401 Unauthorized if token is invalid or missing
    """
    return get_current_user(authorization=authorization)
