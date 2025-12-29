"""
Main entry point for Todo Application.

This file serves as the primary entry point when running:
    python main.py

Launches the interactive menu-driven CLI interface.
"""
import sys

# Add src to path for direct execution
sys.path.insert(0, "src")

from todo_app.interactive import run_interactive


def main():
    """Launch the interactive todo application."""
    run_interactive()


if __name__ == "__main__":
    main()
