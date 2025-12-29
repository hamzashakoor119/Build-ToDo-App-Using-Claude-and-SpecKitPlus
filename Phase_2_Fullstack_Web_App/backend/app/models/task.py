"""Task model for SQLModel ORM."""

from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class TaskBase(SQLModel):
    """Base model with shared fields."""

    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class Task(TaskBase, table=True):
    """Database table model for tasks."""

    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
