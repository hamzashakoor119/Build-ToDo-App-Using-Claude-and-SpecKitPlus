"""
Tests for TaskStore.

Following TDD approach - tests for storage operations.
"""
import pytest
from todo_app.storage import TaskStore
from todo_app.models import Task


class TestTaskStoreAdd:
    """Test adding tasks to store."""

    def test_add_task_returns_id(self):
        """Test that add_task returns a task ID."""
        store = TaskStore()
        task_id = store.add_task("Buy groceries")

        assert task_id is not None
        assert len(task_id) == 36  # UUID format

    def test_add_task_stores_task(self):
        """Test that added task is stored and retrievable."""
        store = TaskStore()
        task_id = store.add_task("Buy groceries")

        task = store.get_task(task_id)
        assert task is not None
        assert task.title == "Buy groceries"

    def test_add_empty_title_raises_error(self):
        """Test that adding empty title raises ValueError."""
        store = TaskStore()

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            store.add_task("")

    def test_add_long_title_raises_error(self):
        """Test that title over 200 chars raises ValueError."""
        store = TaskStore()
        long_title = "A" * 201

        with pytest.raises(ValueError, match="Task title exceeds 200 characters"):
            store.add_task(long_title)


class TestTaskStoreList:
    """Test listing tasks."""

    def test_list_tasks_empty(self):
        """Test listing tasks when store is empty."""
        store = TaskStore()
        tasks = store.list_tasks()

        assert tasks == []

    def test_list_tasks_returns_all(self):
        """Test that list_tasks returns all tasks."""
        store = TaskStore()
        store.add_task("Task 1")
        store.add_task("Task 2")
        store.add_task("Task 3")

        tasks = store.list_tasks()
        assert len(tasks) == 3

    def test_list_tasks_maintains_order(self):
        """Test that tasks are listed in insertion order."""
        store = TaskStore()
        store.add_task("First")
        store.add_task("Second")
        store.add_task("Third")

        tasks = store.list_tasks()
        assert tasks[0].title == "First"
        assert tasks[1].title == "Second"
        assert tasks[2].title == "Third"


class TestTaskStoreGet:
    """Test getting tasks by ID."""

    def test_get_task_by_full_id(self):
        """Test getting task by full UUID."""
        store = TaskStore()
        task_id = store.add_task("Buy groceries")

        task = store.get_task(task_id)
        assert task is not None
        assert task.title == "Buy groceries"

    def test_get_task_by_partial_id(self):
        """Test getting task by partial ID (8+ chars)."""
        store = TaskStore()
        task_id = store.add_task("Buy groceries")
        partial_id = task_id[:8]

        task = store.get_task(partial_id)
        assert task is not None
        assert task.title == "Buy groceries"

    def test_get_nonexistent_task_returns_none(self):
        """Test that getting nonexistent task returns None."""
        store = TaskStore()
        task = store.get_task("nonexistent")

        assert task is None


class TestTaskStoreMarkComplete:
    """Test marking tasks complete/incomplete."""

    def test_mark_task_complete(self):
        """Test marking task as complete."""
        store = TaskStore()
        task_id = store.add_task("Buy groceries")

        task = store.mark_complete(task_id, True)
        assert task.completed is True

    def test_mark_task_incomplete(self):
        """Test marking task as incomplete."""
        store = TaskStore()
        task_id = store.add_task("Buy groceries")
        store.mark_complete(task_id, True)

        task = store.mark_complete(task_id, False)
        assert task.completed is False

    def test_mark_nonexistent_task_raises_error(self):
        """Test that marking nonexistent task raises KeyError."""
        store = TaskStore()

        with pytest.raises(KeyError, match="Task with ID .* not found"):
            store.mark_complete("nonexistent", True)


class TestTaskStoreUpdate:
    """Test updating task titles."""

    def test_update_task_title(self):
        """Test updating a task's title."""
        store = TaskStore()
        task_id = store.add_task("Buy groceries")

        task = store.update_task(task_id, "Buy organic groceries")
        assert task.title == "Buy organic groceries"

    def test_update_with_empty_title_raises_error(self):
        """Test that updating with empty title raises ValueError."""
        store = TaskStore()
        task_id = store.add_task("Buy groceries")

        with pytest.raises(ValueError, match="Task title cannot be empty"):
            store.update_task(task_id, "")

    def test_update_nonexistent_task_raises_error(self):
        """Test that updating nonexistent task raises KeyError."""
        store = TaskStore()

        with pytest.raises(KeyError, match="Task with ID .* not found"):
            store.update_task("nonexistent", "New title")


class TestTaskStoreDelete:
    """Test deleting tasks."""

    def test_delete_task(self):
        """Test deleting a task."""
        store = TaskStore()
        task_id = store.add_task("Buy groceries")

        store.delete_task(task_id)
        task = store.get_task(task_id)
        assert task is None

    def test_delete_task_from_list(self):
        """Test that deleted task doesn't appear in list."""
        store = TaskStore()
        task_id = store.add_task("Buy groceries")
        store.add_task("Call dentist")

        store.delete_task(task_id)
        tasks = store.list_tasks()
        assert len(tasks) == 1
        assert tasks[0].title == "Call dentist"

    def test_delete_nonexistent_task_raises_error(self):
        """Test that deleting nonexistent task raises KeyError."""
        store = TaskStore()

        with pytest.raises(KeyError, match="Task with ID .* not found"):
            store.delete_task("nonexistent")


class TestTaskStoreCount:
    """Test counting tasks."""

    def test_count_empty_store(self):
        """Test count on empty store."""
        store = TaskStore()
        assert store.count() == 0

    def test_count_after_adding(self):
        """Test count after adding tasks."""
        store = TaskStore()
        store.add_task("Task 1")
        store.add_task("Task 2")

        assert store.count() == 2

    def test_count_after_deleting(self):
        """Test count after deleting a task."""
        store = TaskStore()
        task_id = store.add_task("Task 1")
        store.add_task("Task 2")
        store.delete_task(task_id)

        assert store.count() == 1
