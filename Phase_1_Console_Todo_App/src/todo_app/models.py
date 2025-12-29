"""
Task model for todo application.

Implements a simple dataclass with validation for task management.
"""
from dataclasses import dataclass, field
from datetime import datetime
import uuid


@dataclass
class Task:
    """
    Represents a single todo item.

    Attributes:
        id: Unique identifier (UUID v4)
        title: Task description (1-200 characters)
        completed: Whether task is complete (default: False)
        created_at: ISO 8601 timestamp of creation
    """
    title: str
    completed: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def __post_init__(self):
        """Validate task data after initialization."""
        # Trim whitespace
        self.title = self.title.strip()

        # Validate title is not empty
        if not self.title:
            raise ValueError("Task title cannot be empty")

        # Validate title length
        if len(self.title) > 200:
            raise ValueError("Task title exceeds 200 characters")
