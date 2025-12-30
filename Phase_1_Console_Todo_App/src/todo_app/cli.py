"""
Command-line interface for todo application.

Implements argparse-based CLI with subcommands for all operations.
"""
import argparse
import sys
from todo_app.storage import TaskStore


# Global task store (in-memory, lost on exit)
store = TaskStore()


def cmd_add(args) -> int:
    """Handle 'add' command."""
    try:
        description = getattr(args, 'description', None)
        task_id = store.add_task(args.title, description)
        print(f"✓ Task added successfully")
        print(f"ID: {task_id[:8]}")
        print(f"Title: {args.title}")
        if description:
            print(f"Description: {description}")
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130


def cmd_list(args) -> int:
    """Handle 'list' command."""
    try:
        tasks = store.list_tasks()

        if not tasks:
            print("No tasks found.")
            return 0

        print(f"Tasks ({len(tasks)}):\n")
        for task in tasks:
            status = "✓" if task.completed else "○"
            print(f"  [{status}] {task.id[:8]}... {task.title}")
            if task.description:
                # Show truncated description (first 50 chars)
                desc = task.description[:50] + "..." if len(task.description) > 50 else task.description
                print(f"      └─ {desc}")
        return 0
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130


def cmd_complete(args) -> int:
    """Handle 'complete' command."""
    try:
        task = store.mark_complete(args.task_id, True)
        print(f"✓ Task marked as complete")
        print(f"ID: {task.id[:8]}")
        print(f"Title: {task.title}")
        return 0
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130


def cmd_incomplete(args) -> int:
    """Handle 'incomplete' command."""
    try:
        task = store.mark_complete(args.task_id, False)
        print(f"✓ Task marked as incomplete")
        print(f"ID: {task.id[:8]}")
        print(f"Title: {task.title}")
        return 0
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130


def cmd_update(args) -> int:
    """Handle 'update' command."""
    try:
        old_task = store.get_task(args.task_id)
        if old_task is None:
            print(f"Error: Task with ID {args.task_id} not found", file=sys.stderr)
            return 1

        old_title = old_task.title
        old_description = old_task.description

        # Get new values (None means don't update)
        new_title = getattr(args, 'new_title', None)
        new_description = getattr(args, 'description', None)

        task = store.update_task(args.task_id, title=new_title, description=new_description)

        print(f"✓ Task updated successfully")
        print(f"ID: {task.id[:8]}")

        if new_title is not None:
            print(f"Old Title: {old_title}")
            print(f"New Title: {task.title}")
        else:
            print(f"Title: {task.title}")

        if new_description is not None:
            if old_description:
                print(f"Old Description: {old_description}")
            if task.description:
                print(f"New Description: {task.description}")
            else:
                print(f"Description: (cleared)")

        return 0
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130


def cmd_delete(args) -> int:
    """Handle 'delete' command."""
    try:
        task = store.get_task(args.task_id)
        if task is None:
            print(f"Error: Task with ID {args.task_id} not found", file=sys.stderr)
            return 1

        title = task.title
        task_id_short = task.id[:8]
        store.delete_task(args.task_id)

        print(f"✓ Task deleted successfully")
        print(f"ID: {task_id_short}")
        print(f"Title: {title}")
        return 0
    except KeyError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nCancelled.", file=sys.stderr)
        return 130


def get_version() -> str:
    """Get application version from package metadata."""
    try:
        from importlib.metadata import version
        return version("todo-app")
    except Exception:
        return "0.1.0"


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        description="Simple console todo application",
        prog="todo"
    )
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {get_version()}"
    )

    subparsers = parser.add_subparsers(dest="command", required=False)

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new task")
    add_parser.add_argument("title", help="Task title")
    add_parser.add_argument(
        "-d", "--description",
        help="Task description (optional)",
        default=None
    )
    add_parser.set_defaults(func=cmd_add)

    # List command
    list_parser = subparsers.add_parser("list", help="List all tasks")
    list_parser.set_defaults(func=cmd_list)

    # Complete command
    complete_parser = subparsers.add_parser("complete", help="Mark task as complete")
    complete_parser.add_argument("task_id", help="Task ID (full or partial, min 8 chars)")
    complete_parser.set_defaults(func=cmd_complete)

    # Incomplete command
    incomplete_parser = subparsers.add_parser("incomplete", help="Mark task as incomplete")
    incomplete_parser.add_argument("task_id", help="Task ID (full or partial, min 8 chars)")
    incomplete_parser.set_defaults(func=cmd_incomplete)

    # Update command
    update_parser = subparsers.add_parser("update", help="Update task title and/or description")
    update_parser.add_argument("task_id", help="Task ID (full or partial, min 8 chars)")
    update_parser.add_argument("new_title", nargs="?", default=None, help="New task title (optional)")
    update_parser.add_argument(
        "-d", "--description",
        help="New task description (use empty string to clear)",
        default=None
    )
    update_parser.set_defaults(func=cmd_update)

    # Delete command
    delete_parser = subparsers.add_parser("delete", help="Delete a task")
    delete_parser.add_argument("task_id", help="Task ID (full or partial, min 8 chars)")
    delete_parser.set_defaults(func=cmd_delete)

    return parser


def run_cli(args=None) -> int:
    """
    Run the CLI with given arguments.

    Args:
        args: Command-line arguments (uses sys.argv if None)

    Returns:
        int: Exit code (0 for success, non-zero for error)
    """
    parser = create_parser()
    parsed_args = parser.parse_args(args)

    # If no command provided, show help
    if parsed_args.command is None:
        parser.print_help()
        return 0

    # Call the appropriate command function
    return parsed_args.func(parsed_args)
