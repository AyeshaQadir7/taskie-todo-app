"""Pydantic request and response models"""
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel
from pydantic import Field


class TaskCreate(SQLModel):
    """Request model for POST /api/{user_id}/tasks"""
    title: str = Field(
        min_length=1,
        max_length=255,
        description="Task title (required)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Extended task description (optional)"
    )


class TaskUpdate(SQLModel):
    """Request model for PUT /api/{user_id}/tasks/{id}"""
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=255,
        description="Task title (optional)"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Extended task description (optional)"
    )


class TaskResponse(SQLModel):
    """Response model for all GET/POST/PUT/PATCH endpoints"""
    id: int
    user_id: str
    title: str
    description: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime


class ErrorResponse(SQLModel):
    """Standard error response for all error cases"""
    error: str
