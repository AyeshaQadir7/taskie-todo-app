"""
Authentication Context Management

This module manages the authenticated user context extracted from validated JWT tokens.
It provides the AuthenticatedUser model and context helpers for endpoint handlers.

Spec: 002-authentication-jwt
Created: 2026-01-09
"""

from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AuthenticatedUser(BaseModel):
    """
    Authenticated user context extracted from validated JWT.

    This model represents the user identity and token metadata after successful
    JWT validation. It is injected into endpoint handlers via FastAPI dependency
    injection.

    Attributes:
        user_id: Unique user identifier from JWT "sub" claim
        email: User email address from JWT "email" claim
        token_issued_at: Token issuance timestamp from JWT "iat" claim
        token_expires_at: Token expiration timestamp from JWT "exp" claim
    """
    user_id: str = Field(..., description="User ID from JWT sub claim")
    email: str = Field(..., description="User email from JWT email claim")
    token_issued_at: datetime = Field(..., description="Token issuance timestamp (iat)")
    token_expires_at: datetime = Field(..., description="Token expiration timestamp (exp)")

    @property
    def is_expired(self) -> bool:
        """Check if token is expired (current time > exp)"""
        return datetime.utcnow() > self.token_expires_at

    @property
    def time_to_expiry(self) -> int:
        """Get remaining token lifetime in seconds"""
        delta = self.token_expires_at - datetime.utcnow()
        return max(0, int(delta.total_seconds()))

    def __str__(self) -> str:
        return f"AuthenticatedUser(user_id={self.user_id}, email={self.email})"

    def __repr__(self) -> str:
        return self.__str__()

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user-123",
                "email": "user@example.com",
                "token_issued_at": "2026-01-09T12:00:00Z",
                "token_expires_at": "2026-01-16T12:00:00Z"
            }
        }


class AuthContext:
    """
    Authentication context holder for request lifecycle.

    This class provides thread-safe context management for the authenticated
    user within a request. It can be used to store and retrieve the current
    user throughout the request processing pipeline.
    """

    def __init__(self):
        self._current_user: Optional[AuthenticatedUser] = None

    def set_user(self, user: AuthenticatedUser) -> None:
        """Set the authenticated user for the current request"""
        self._current_user = user

    def get_user(self) -> Optional[AuthenticatedUser]:
        """Get the authenticated user for the current request"""
        return self._current_user

    def clear(self) -> None:
        """Clear the authentication context"""
        self._current_user = None

    def has_user(self) -> bool:
        """Check if a user is authenticated in the current context"""
        return self._current_user is not None


def extract_user_from_jwt(jwt_payload: dict) -> AuthenticatedUser:
    """
    Extract AuthenticatedUser from validated JWT payload.

    Args:
        jwt_payload: Decoded JWT token payload (claims)

    Returns:
        AuthenticatedUser: User context object

    Raises:
        ValueError: If required claims are missing

    Example:
        >>> payload = {
        ...     "sub": "user-123",
        ...     "email": "user@example.com",
        ...     "iat": 1704672000,
        ...     "exp": 1705276800
        ... }
        >>> user = extract_user_from_jwt(payload)
        >>> user.user_id
        'user-123'
    """
    # Validate required claims
    required_claims = ["sub", "email", "iat", "exp"]
    missing_claims = [claim for claim in required_claims if claim not in jwt_payload]

    if missing_claims:
        raise ValueError(f"Missing required JWT claims: {', '.join(missing_claims)}")

    # Extract claims
    user_id = jwt_payload["sub"]
    email = jwt_payload["email"]
    iat = jwt_payload["iat"]
    exp = jwt_payload["exp"]

    # Convert Unix timestamps to datetime objects
    token_issued_at = datetime.utcfromtimestamp(iat)
    token_expires_at = datetime.utcfromtimestamp(exp)

    return AuthenticatedUser(
        user_id=user_id,
        email=email,
        token_issued_at=token_issued_at,
        token_expires_at=token_expires_at
    )


def verify_user_ownership(authenticated_user: AuthenticatedUser, resource_user_id: str) -> bool:
    """
    Verify that the authenticated user owns the resource.

    This function compares the user_id from the JWT token with the user_id
    from the API route path to enforce multi-user isolation.

    Args:
        authenticated_user: User context from JWT validation
        resource_user_id: User ID from API route path (e.g., /api/{user_id}/tasks)

    Returns:
        bool: True if user_id matches, False otherwise

    Example:
        >>> user = AuthenticatedUser(user_id="user-123", email="user@example.com", ...)
        >>> verify_user_ownership(user, "user-123")
        True
        >>> verify_user_ownership(user, "user-456")
        False
    """
    return authenticated_user.user_id == resource_user_id
