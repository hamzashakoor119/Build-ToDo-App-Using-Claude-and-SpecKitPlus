"""
Main entry point for todo application.
"""
import sys
from todo_app.cli import run_cli


def main() -> int:
    """Main entry point."""
    return run_cli()


if __name__ == "__main__":
    sys.exit(main())
