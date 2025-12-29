# Phase 1: Console Todo App

A simple, interactive command-line todo application built with Python.

## Features

- Add, view, update, and delete tasks
- Mark tasks as complete/incomplete
- Interactive CLI with menu-driven interface
- JSON file-based storage
- Full test coverage

## Requirements

- Python 3.13+
- uv (recommended) or pip

## Quick Start

```bash
# Navigate to this directory
cd Phase_1_Console_Todo_App

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync

# Run the app
uv run python -m todo_app
# OR
uv run todo
```

## Running Tests

```bash
uv run pytest
```

## Project Structure

```
Phase_1_Console_Todo_App/
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py          # CLI argument parser
│       ├── interactive.py  # Interactive menu
│       ├── main.py         # Entry point
│       ├── models.py       # Task data model
│       └── storage.py      # JSON file storage
├── tests/
├── pyproject.toml
└── README.md
```

## Usage

The app provides an interactive menu with the following options:

1. **Add Task** - Create a new task with title and optional description
2. **List Tasks** - View all tasks (pending and completed)
3. **Update Task** - Modify task title or description
4. **Delete Task** - Remove a task
5. **Toggle Complete** - Mark task as complete/incomplete
6. **Exit** - Close the application

## Storage

Tasks are stored in `todos.json` in the current directory.
