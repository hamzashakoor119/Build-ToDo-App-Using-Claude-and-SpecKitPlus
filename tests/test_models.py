"""
Tests for Task model.

Following TDD approach - these tests should FAIL first,
then pass after implementing the Task dataclass.
"""
import pytest
from datetime import datetime
from todo_app.models import Task


class TestTaskCreation:
    """Test Task dataclass creation and default values."""

    def test_task_creation_with_title(self):
        """Test creating a task with just a title."""
        task = Task(title="Buy groceries")

        assert task.title == "Buy groceries"
        assert task.completed is False
        assert task.id is not None
        assert len(task.id) == 36  # UUID v4 format: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
        assert task.created_at is not None

    def test_task_id_is_unique(self):
        """Test that each task gets a unique ID."""
        task1 = Task(title="Task 1")
        task2 = Task(title="Task 2")

        assert task1.id != task2.id

    def test_task_created_at_is_iso_format(self):
        """Test that created_at is in ISO 8601 format."""
        task = Task(title="Test task")

        # Should be parseable as ISO 8601
        datetime.fromisoformat(task.created_at)
        assert "T" in task.created_at  # ISO format includes 'T'


class TestTaskValidation:
    """Test Task validation rules."""

    def test_empty_title_raises_error(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(title="")

    def test_whitespace_only_title_raises_error(self):
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task(title="   ")

    def test_title_too_long_raises_error(self):
        """Test that title exceeding 200 characters raises ValueError."""
        long_title = "A" * 201
        with pytest.raises(ValueError, match="Task title exceeds 200 characters"):
            Task(title=long_title)

    def test_title_exactly_200_chars_is_valid(self):
        """Test that title with exactly 200 characters is valid."""
        title_200 = "A" * 200
        task = Task(title=title_200)

        assert task.title == title_200

    def test_title_is_trimmed(self):
        """Test that leading/trailing whitespace is trimmed."""
        task = Task(title="  Buy groceries  ")

        assert task.title == "Buy groceries"


class TestTaskCompletion:
    """Test Task completion status."""

    def test_task_defaults_to_incomplete(self):
        """Test that new tasks are incomplete by default."""
        task = Task(title="Test task")

        assert task.completed is False

    def test_task_can_be_created_as_completed(self):
        """Test that tasks can be created with completed=True."""
        task = Task(title="Test task", completed=True)

        assert task.completed is True


class TestTaskEdgeCases:
    """Test edge cases and special characters."""

    def test_title_with_special_characters(self):
        """Test that special characters are allowed in titles."""
        task = Task(title="Buy 🛒 groceries & snacks!")

        assert task.title == "Buy 🛒 groceries & snacks!"

    def test_title_with_quotes(self):
        """Test that quotes are allowed in titles."""
        task = Task(title='Read "Python Guide"')

        assert task.title == 'Read "Python Guide"'

    def test_single_character_title(self):
        """Test that single character titles are valid."""
        task = Task(title="A")

        assert task.title == "A"
