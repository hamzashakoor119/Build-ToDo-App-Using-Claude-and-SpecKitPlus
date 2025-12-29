"""
Allow running todo_app as a module: python -m todo_app

Usage:
    python -m todo_app              # Interactive mode (menu-driven)
    python -m todo_app add "Task"   # CLI mode with subcommands
    python -m todo_app list         # CLI mode - list tasks
    python -m todo_app --help       # Show CLI help
"""
import sys
from todo_app.cli import run_cli
from todo_app.interactive import run_interactive


def main() -> int:
    """
    Main entry point with dual-mode support.

    - No arguments: Launch interactive menu
    - With arguments: Run CLI command
    """
    # If no arguments (or only script name), run interactive mode
    if len(sys.argv) == 1:
        run_interactive()
        return 0

    # Otherwise, run CLI mode
    return run_cli()


if __name__ == "__main__":
    sys.exit(main())
