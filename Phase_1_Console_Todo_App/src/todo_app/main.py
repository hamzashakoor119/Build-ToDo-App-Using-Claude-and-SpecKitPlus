"""
Main entry point for todo application.

This module provides dual-mode operation:
- Interactive mode: Menu-driven interface (default when no arguments)
- CLI mode: Command-line arguments for scripting

Usage:
    todo                    # Interactive mode
    todo add "Buy milk"     # CLI mode
    todo list               # CLI mode
    todo --help             # Show help
"""
import sys
from todo_app.cli import run_cli
from todo_app.interactive import run_interactive


def main() -> int:
    """
    Main entry point with dual-mode support.

    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    # If no arguments, run interactive mode
    if len(sys.argv) == 1:
        run_interactive()
        return 0

    # Otherwise, run CLI mode with arguments
    return run_cli()


if __name__ == "__main__":
    sys.exit(main())
