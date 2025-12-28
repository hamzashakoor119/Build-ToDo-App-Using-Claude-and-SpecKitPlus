"""Task schemas for API request/response validation."""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class TaskCreate(SQLModel):
    """Schema for creating a task."""

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskUpdate(SQLModel):
    """Schema for updating a task (all fields optional)."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskRead(SQLModel):
    """Schema for reading a task."""

    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime
