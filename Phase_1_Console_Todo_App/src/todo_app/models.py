"""
Task model for todo application.

Implements a simple dataclass with validation for task management.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
import uuid


@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique identifier (UUID v4)
        title: Task title (1-200 characters, required)
        description: Task description (optional, up to 1000 characters)
        completed: Whether task is complete (default: False)
        created_at: ISO 8601 timestamp of creation
    """
    title: str
    description: Optional[str] = None
    completed: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        """Validate task data after initialization."""
        # Trim whitespace from title
        self.title = self.title.strip()

        # Validate title is not empty
        if not self.title:
            raise ValueError("Task title cannot be empty")

        # Validate title length
        if len(self.title) > 200:
            raise ValueError("Task title exceeds 200 characters")

        # Validate and clean description
        if self.description is not None:
            self.description = self.description.strip()
            # Empty description becomes None
            if not self.description:
                self.description = None
            elif len(self.description) > 1000:
                raise ValueError("Task description exceeds 1000 characters")
