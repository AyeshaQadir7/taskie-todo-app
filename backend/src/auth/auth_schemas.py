"""
Authentication Schemas for JWT-based Authentication

This module defines Pydantic schemas for authentication requests, responses,
and error handling. These schemas enforce validation for JWT tokens and
authentication-related data structures.

Spec: 002-authentication-jwt
Created: 2026-01-09
"""

from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator


class SignUpRequest(BaseModel):
    """
    Sign-up request schema (handled by Better Auth on frontend).
    This schema documents the expected format for reference.
    """
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")


class SignInRequest(BaseModel):
    """
    Sign-in request schema (handled by Better Auth on frontend).
    This schema documents the expected format for reference.
    """
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """
    JWT token response from Better Auth.
    This schema documents the expected response format.
    """
    token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="Bearer", description="Token type (RFC 6750)")
    expires_in: int = Field(..., description="Token expiration time in seconds (7 days = 604800)")


class AuthError(BaseModel):
    """
    Authentication error response.
    Returned when JWT validation fails (401 Unauthorized).
    """
    detail: str = Field(default="Unauthorized", description="Error category")
    message: str = Field(..., description="Specific error message")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "detail": "Unauthorized",
                    "message": "Invalid token"
                },
                {
                    "detail": "Unauthorized",
                    "message": "Token expired"
                },
                {
                    "detail": "Unauthorized",
                    "message": "Missing authorization header"
                }
            ]
        }


class AuthorizationError(BaseModel):
    """
    Authorization error response.
    Returned when user attempts to access resources they don't own (403 Forbidden).
    """
    detail: str = Field(default="Forbidden", description="Error category")
    message: str = Field(..., description="Specific error message")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "detail": "Forbidden",
                    "message": "Access denied"
                },
                {
                    "detail": "Forbidden",
                    "message": "User ID mismatch"
                }
            ]
        }


class JWTPayload(BaseModel):
    """
    JWT token payload structure (claims).
    This represents the decoded JWT token content.
    """
    sub: str = Field(..., description="Subject: User ID")
    email: str = Field(..., description="User email address")
    iat: int = Field(..., description="Issued at time (Unix timestamp)")
    exp: int = Field(..., description="Expiration time (Unix timestamp)")
    iss: Optional[str] = Field(default="better-auth", description="Issuer")
    aud: Optional[str] = Field(default="taskie-api", description="Audience")

    @validator("exp", "iat")
    def validate_timestamp(cls, v):
        """Ensure timestamps are positive integers"""
        if v < 0:
            raise ValueError("Timestamp must be positive")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "sub": "user-123",
                "email": "user@example.com",
                "iat": 1704672000,
                "exp": 1705276800,
                "iss": "better-auth",
                "aud": "taskie-api"
            }
        }


class AuthenticatedUser(BaseModel):
    """
    Authenticated user context extracted from validated JWT.
    This is passed to endpoint handlers after successful JWT validation.
    """
    user_id: str = Field(..., description="User ID from JWT sub claim")
    email: str = Field(..., description="User email from JWT email claim")
    token_issued_at: int = Field(..., description="Token issuance timestamp (iat)")
    token_expires_at: int = Field(..., description="Token expiration timestamp (exp)")

    class Config:
        json_schema_extra = {
            "example": {
                "user_id": "user-123",
                "email": "user@example.com",
                "token_issued_at": 1704672000,
                "token_expires_at": 1705276800
            }
        }


class ValidationError(BaseModel):
    """
    Validation error response (422 Unprocessable Entity).
    Returned when request data fails validation.
    """
    detail: str = Field(default="Validation error", description="Error category")
    errors: list = Field(..., description="List of validation errors")
