"""
Tests for CLI commands.

Integration tests for command-line interface.
"""
import pytest
from todo_app.cli import run_cli, store


@pytest.fixture(autouse=True)
def reset_store():
    """Reset store before each test."""
    store._tasks.clear()
    store._order.clear()


class TestCLIAdd:
    """Test 'add' command."""

    def test_add_command(self, capsys):
        """Test adding a task via CLI."""
        exit_code = run_cli(["add", "Buy groceries"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "✓ Task added successfully" in captured.out
        assert "Buy groceries" in captured.out

    def test_add_empty_title_shows_error(self, capsys):
        """Test adding empty title shows error."""
        exit_code = run_cli(["add", ""])

        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error:" in captured.err
        assert "cannot be empty" in captured.err

    def test_add_with_description(self, capsys):
        """Test adding a task with description."""
        exit_code = run_cli(["add", "Buy groceries", "-d", "Milk, eggs, bread"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "✓ Task added successfully" in captured.out
        assert "Buy groceries" in captured.out
        assert "Milk, eggs, bread" in captured.out

    def test_add_with_long_description_flag(self, capsys):
        """Test adding a task with --description flag."""
        exit_code = run_cli(["add", "Buy groceries", "--description", "Shopping list"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "Shopping list" in captured.out


class TestCLIList:
    """Test 'list' command."""

    def test_list_empty(self, capsys):
        """Test listing with no tasks."""
        exit_code = run_cli(["list"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "No tasks found" in captured.out

    def test_list_with_tasks(self, capsys):
        """Test listing with tasks."""
        run_cli(["add", "Task 1"])
        run_cli(["add", "Task 2"])

        exit_code = run_cli(["list"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "Tasks (2)" in captured.out
        assert "Task 1" in captured.out
        assert "Task 2" in captured.out

    def test_list_shows_completion_status(self, capsys):
        """Test that list shows completion symbols."""
        task_id = store.add_task("Test task")
        store.mark_complete(task_id, True)

        exit_code = run_cli(["list"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "✓" in captured.out  # Completed symbol
        assert "Test task" in captured.out

    def test_list_shows_description(self, capsys):
        """Test that list shows task descriptions."""
        store.add_task("Buy groceries", "Milk, eggs, bread")

        exit_code = run_cli(["list"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "Buy groceries" in captured.out
        assert "Milk, eggs, bread" in captured.out


class TestCLIComplete:
    """Test 'complete' command."""

    def test_complete_task(self, capsys):
        """Test marking task as complete."""
        task_id = store.add_task("Buy groceries")
        partial_id = task_id[:8]

        exit_code = run_cli(["complete", partial_id])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "✓ Task marked as complete" in captured.out

        task = store.get_task(task_id)
        assert task.completed is True

    def test_complete_nonexistent_task(self, capsys):
        """Test completing nonexistent task shows error."""
        exit_code = run_cli(["complete", "nonexistent"])

        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error:" in captured.err


class TestCLIIncomplete:
    """Test 'incomplete' command."""

    def test_incomplete_task(self, capsys):
        """Test marking task as incomplete."""
        task_id = store.add_task("Buy groceries")
        store.mark_complete(task_id, True)
        partial_id = task_id[:8]

        exit_code = run_cli(["incomplete", partial_id])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "✓ Task marked as incomplete" in captured.out

        task = store.get_task(task_id)
        assert task.completed is False


class TestCLIUpdate:
    """Test 'update' command."""

    def test_update_task(self, capsys):
        """Test updating task title."""
        task_id = store.add_task("Buy groceries")
        partial_id = task_id[:8]

        exit_code = run_cli(["update", partial_id, "Buy organic groceries"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "✓ Task updated successfully" in captured.out
        assert "Old Title: Buy groceries" in captured.out
        assert "New Title: Buy organic groceries" in captured.out

        task = store.get_task(task_id)
        assert task.title == "Buy organic groceries"

    def test_update_nonexistent_task(self, capsys):
        """Test updating nonexistent task shows error."""
        exit_code = run_cli(["update", "nonexistent", "New title"])

        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error:" in captured.err

    def test_update_task_description(self, capsys):
        """Test updating task description."""
        task_id = store.add_task("Buy groceries")
        partial_id = task_id[:8]

        exit_code = run_cli(["update", partial_id, "-d", "Milk, eggs, bread"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "✓ Task updated successfully" in captured.out
        assert "New Description: Milk, eggs, bread" in captured.out

        task = store.get_task(task_id)
        assert task.description == "Milk, eggs, bread"

    def test_update_task_title_and_description(self, capsys):
        """Test updating both title and description."""
        task_id = store.add_task("Buy groceries", "Old items")
        partial_id = task_id[:8]

        exit_code = run_cli(["update", partial_id, "Buy organic groceries", "-d", "New items"])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "✓ Task updated successfully" in captured.out

        task = store.get_task(task_id)
        assert task.title == "Buy organic groceries"
        assert task.description == "New items"

    def test_update_clear_description(self, capsys):
        """Test clearing description with empty string."""
        task_id = store.add_task("Buy groceries", "Some description")
        partial_id = task_id[:8]

        exit_code = run_cli(["update", partial_id, "-d", ""])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "(cleared)" in captured.out

        task = store.get_task(task_id)
        assert task.description is None


class TestCLIDelete:
    """Test 'delete' command."""

    def test_delete_task(self, capsys):
        """Test deleting a task."""
        task_id = store.add_task("Buy groceries")
        partial_id = task_id[:8]

        exit_code = run_cli(["delete", partial_id])

        captured = capsys.readouterr()
        assert exit_code == 0
        assert "✓ Task deleted successfully" in captured.out

        task = store.get_task(task_id)
        assert task is None

    def test_delete_nonexistent_task(self, capsys):
        """Test deleting nonexistent task shows error."""
        exit_code = run_cli(["delete", "nonexistent"])

        captured = capsys.readouterr()
        assert exit_code == 1
        assert "Error:" in captured.err
