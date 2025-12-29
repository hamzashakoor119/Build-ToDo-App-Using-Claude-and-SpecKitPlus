"""
In-memory task storage.

Implements TaskStore class using Dict + List pattern for O(1) lookups
while maintaining insertion order.
"""
from typing import Dict, List, Optional
from todo_app.models import Task


class TaskStore:
    """
    In-memory storage for tasks.

    Uses Dict for O(1) lookups by ID and List to maintain insertion order.
    """

    def __init__(self):
        """Initialize empty task store."""
        self._tasks: Dict[str, Task] = {}
        self._order: List[str] = []

    def add_task(self, title: str) -> str:
        """
        Add a new task and return its ID.

        Args:
            title: Task title (will be validated by Task model)

        Returns:
            str: The UUID of the created task

        Raises:
            ValueError: If title is invalid (empty or too long)
        """
        task = Task(title=title)
        self._tasks[task.id] = task
        self._order.append(task.id)
        return task.id

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Get a task by ID.

        Args:
            task_id: Full or partial task ID (minimum 8 characters)

        Returns:
            Task if found, None otherwise

        Raises:
            ValueError: If partial ID matches multiple tasks
        """
        # Try exact match first
        if task_id in self._tasks:
            return self._tasks[task_id]

        # Try partial match (minimum 8 characters)
        if len(task_id) >= 8:
            matches = [tid for tid in self._tasks.keys() if tid.startswith(task_id)]
            if len(matches) == 1:
                return self._tasks[matches[0]]
            elif len(matches) > 1:
                raise ValueError(f"Ambiguous task ID '{task_id}' matches multiple tasks")

        return None

    def list_tasks(self) -> List[Task]:
        """
        List all tasks in insertion order.

        Returns:
            List of all tasks
        """
        return [self._tasks[tid] for tid in self._order if tid in self._tasks]

    def mark_complete(self, task_id: str, completed: bool = True) -> Task:
        """
        Mark a task as complete or incomplete.

        Args:
            task_id: Full or partial task ID
            completed: True to mark complete, False for incomplete

        Returns:
            The updated task

        Raises:
            KeyError: If task not found
        """
        task = self.get_task(task_id)
        if task is None:
            raise KeyError(f"Task with ID {task_id} not found")

        task.completed = completed
        return task

    def update_task(self, task_id: str, title: str) -> Task:
        """
        Update a task's title.

        Args:
            task_id: Full or partial task ID
            title: New title (will be validated)

        Returns:
            The updated task

        Raises:
            KeyError: If task not found
            ValueError: If title is invalid
        """
        task = self.get_task(task_id)
        if task is None:
            raise KeyError(f"Task with ID {task_id} not found")

        # Validate new title by creating temporary task
        temp = Task(title=title)

        # Update the title
        task.title = temp.title
        return task

    def delete_task(self, task_id: str) -> None:
        """
        Delete a task permanently.

        Args:
            task_id: Full or partial task ID

        Raises:
            KeyError: If task not found
        """
        task = self.get_task(task_id)
        if task is None:
            raise KeyError(f"Task with ID {task_id} not found")

        # Remove from dict and order list
        del self._tasks[task.id]
        self._order.remove(task.id)

    def count(self) -> int:
        """
        Return the total number of tasks.

        Returns:
            int: Number of tasks
        """
        return len(self._tasks)
