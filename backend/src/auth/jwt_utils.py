"""
JWT Utility Functions

This module provides JWT token parsing, verification, and claims extraction
utilities using the PyJWT library. All functions implement stateless JWT
validation using the shared BETTER_AUTH_SECRET.

Spec: 002-authentication-jwt
Created: 2026-01-09
"""

import jwt
import os
from typing import Dict, Optional
from datetime import datetime, timedelta
from jwt.exceptions import (
    InvalidTokenError,
    ExpiredSignatureError,
    InvalidSignatureError,
    DecodeError
)


# JWT Configuration
JWT_ALGORITHM = "HS256"  # HMAC with SHA-256 (symmetric key)
JWT_SECRET_ENV_VAR = "BETTER_AUTH_SECRET"


def get_jwt_secret() -> str:
    """
    Retrieve JWT secret from environment variable.

    Returns:
        str: JWT secret for signing/verification

    Raises:
        ValueError: If BETTER_AUTH_SECRET is not configured
    """
    secret = os.getenv(JWT_SECRET_ENV_VAR)

    if not secret:
        raise ValueError(
            f"{JWT_SECRET_ENV_VAR} environment variable is not configured. "
            "This secret is required for JWT validation. "
            "Generate a secure secret with: openssl rand -base64 48"
        )

    if len(secret) < 32:
        raise ValueError(
            f"{JWT_SECRET_ENV_VAR} must be at least 32 characters long. "
            f"Current length: {len(secret)} characters."
        )

    return secret


def parse_bearer_token(authorization_header: Optional[str]) -> Optional[str]:
    """
    Extract JWT token from Authorization header.

    Args:
        authorization_header: HTTP Authorization header value

    Returns:
        Optional[str]: Extracted JWT token, or None if invalid format

    Example:
        >>> parse_bearer_token("Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...'
        >>> parse_bearer_token("Invalid")
        None
    """
    if not authorization_header:
        return None

    # Expected format: "Bearer <token>"
    parts = authorization_header.split()

    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    return parts[1]


def verify_jwt_token(token: str, secret: Optional[str] = None) -> Dict:
    """
    Verify JWT token signature and expiration.

    This function performs stateless JWT validation:
    1. Verify signature using BETTER_AUTH_SECRET with explicit algorithm check
    2. Verify issuer (iss) and audience (aud) claims
    3. Verify token is not expired (exp claim)
    4. Return decoded payload (claims)

    Args:
        token: JWT token string
        secret: JWT secret (defaults to BETTER_AUTH_SECRET from env)

    Returns:
        Dict: Decoded JWT payload (claims)

    Raises:
        ExpiredSignatureError: Token has expired
        InvalidSignatureError: Token signature is invalid
        InvalidTokenError: Token is malformed or invalid

    Example:
        >>> token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        >>> payload = verify_jwt_token(token)
        >>> payload["sub"]
        'user-123'
    """
    if secret is None:
        secret = get_jwt_secret()

    try:
        # First, decode without verification to inspect the header
        # This allows us to validate the algorithm before processing
        unverified_header = jwt.get_unverified_header(token)

        # SECURITY: Prevent algorithm confusion attacks
        if unverified_header.get("alg") != JWT_ALGORITHM:
            raise InvalidSignatureError(
                f"Algorithm mismatch: expected {JWT_ALGORITHM}, "
                f"got {unverified_header.get('alg')}"
            )

        # Decode and verify token with explicit issuer/audience validation
        # PyJWT automatically verifies signature and expiration
        payload = jwt.decode(
            token,
            secret,
            algorithms=[JWT_ALGORITHM],
            audience="taskie-api",  # Verify aud claim
            issuer="better-auth",   # Verify iss claim
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_aud": True,
                "verify_iss": True,
                "require": ["sub", "email", "iat", "exp", "iss", "aud"]
            }
        )

        return payload

    except ExpiredSignatureError:
        # Token has expired
        raise ExpiredSignatureError("Token expired")

    except InvalidSignatureError:
        # Token signature is invalid (wrong secret or tampered token)
        raise InvalidSignatureError("Invalid token signature")

    except DecodeError:
        # Token is malformed (not a valid JWT)
        raise DecodeError("Invalid token format")

    except InvalidTokenError as e:
        # Other JWT validation errors
        raise InvalidTokenError(f"Invalid token: {str(e)}")


def extract_user_id_from_token(token: str) -> str:
    """
    Extract user_id from JWT token without full validation.

    This is a convenience function for extracting the user_id claim.
    Use verify_jwt_token() for full validation.

    Args:
        token: JWT token string

    Returns:
        str: User ID from "sub" claim

    Raises:
        InvalidTokenError: If token cannot be decoded or "sub" claim is missing
    """
    try:
        # Decode without verification (for inspection only)
        payload = jwt.decode(token, options={"verify_signature": False})

        if "sub" not in payload:
            raise InvalidTokenError("Token missing 'sub' claim")

        return payload["sub"]

    except Exception as e:
        raise InvalidTokenError(f"Cannot extract user_id: {str(e)}")


def is_token_expired(token: str) -> bool:
    """
    Check if JWT token is expired without full validation.

    Args:
        token: JWT token string

    Returns:
        bool: True if token is expired, False otherwise
    """
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        exp = payload.get("exp")

        if not exp:
            return True

        expiration_time = datetime.utcfromtimestamp(exp)
        return datetime.utcnow() > expiration_time

    except Exception:
        return True  # Treat invalid tokens as expired


def get_token_expiration(token: str) -> Optional[datetime]:
    """
    Get expiration time from JWT token.

    Args:
        token: JWT token string

    Returns:
        Optional[datetime]: Token expiration time, or None if cannot be determined
    """
    try:
        payload = jwt.decode(token, options={"verify_signature": False})
        exp = payload.get("exp")

        if exp:
            return datetime.utcfromtimestamp(exp)

        return None

    except Exception:
        return None


def create_test_jwt_token(
    user_id: str,
    email: str,
    expires_in_seconds: int = 604800,  # 7 days
    secret: Optional[str] = None
) -> str:
    """
    Create a test JWT token for testing purposes.

    This function is used in tests to generate valid JWT tokens.
    DO NOT use this in production - Better Auth generates tokens on frontend.

    Args:
        user_id: User ID for "sub" claim
        email: User email for "email" claim
        expires_in_seconds: Token lifetime in seconds (default: 7 days)
        secret: JWT secret (defaults to BETTER_AUTH_SECRET from env)

    Returns:
        str: Encoded JWT token

    Example:
        >>> token = create_test_jwt_token("user-123", "user@example.com")
        >>> payload = verify_jwt_token(token)
        >>> payload["sub"]
        'user-123'
    """
    if secret is None:
        secret = get_jwt_secret()

    now = datetime.utcnow()
    expiration = now + timedelta(seconds=expires_in_seconds)

    payload = {
        "sub": user_id,
        "email": email,
        "iat": int(now.timestamp()),
        "exp": int(expiration.timestamp()),
        "iss": "better-auth",
        "aud": "taskie-api"
    }

    token = jwt.encode(payload, secret, algorithm=JWT_ALGORITHM)

    return token
