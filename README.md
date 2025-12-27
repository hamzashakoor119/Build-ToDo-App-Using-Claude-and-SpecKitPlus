# Console Todo Application

A simple command-line todo application built with Python 3.13+ using Test-Driven Development (TDD) principles.

## Features

- **Add tasks**: Create new todo items
- **View tasks**: List all tasks with completion status
- **Mark complete**: Toggle task completion status
- **Update tasks**: Modify task titles
- **Delete tasks**: Remove tasks permanently

## Requirements

- Python 3.13 or higher
- UV package manager

## Installation

### 1. Install UV

```bash
# Linux/macOS
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Install Dependencies

```bash
# Install project with dev dependencies
uv sync
```

## Usage

### Add a Task

```bash
uv run python -m todo_app.main add "Buy groceries"
```

### List All Tasks

```bash
uv run python -m todo_app.main list
```

Output format:
```
Tasks (3):
  [○] f47ac10b... Buy groceries
  [✓] a3f2c1b0... Write documentation
  [○] 12345678... Call dentist
```

### Mark Task as Complete

```bash
# Using partial ID (minimum 8 characters)
uv run python -m todo_app.main complete f47ac10b
```

### Mark Task as Incomplete

```bash
uv run python -m todo_app.main incomplete f47ac10b
```

### Update Task Title

```bash
uv run python -m todo_app.main update f47ac10b "Buy organic groceries"
```

### Delete a Task

```bash
uv run python -m todo_app.main delete f47ac10b
```

## Development

### Run Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=todo_app --cov-report=term-missing

# Run specific test file
uv run pytest tests/test_models.py
```

### Project Structure

```
todo-app/
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── models.py       # Task dataclass
│       ├── storage.py      # In-memory TaskStore
│       ├── cli.py          # CLI commands
│       └── main.py         # Entry point
├── tests/
│   ├── __init__.py
│   ├── test_models.py      # Task model tests
│   ├── test_storage.py     # Storage tests
│   └── test_cli.py         # CLI integration tests
├── specs/                  # Design documents
├── pyproject.toml          # Project configuration
└── README.md
```

## Important Notes

### Data Persistence

⚠️ **In-Memory Storage**: All tasks are stored in memory and **lost when the application exits**. This is by design for Phase I.

- Each command execution is a separate session
- Tasks exist only during runtime
- Future phases will add persistent storage (database)

### Task IDs

- Tasks are identified by UUID v4
- You can use partial IDs (minimum 8 characters)
- Example: `f47ac10b` instead of full `f47ac10b-58cc-4372-a567-0e02b2c3d479`

## Technical Details

- **Language**: Python 3.13+
- **CLI Framework**: argparse (built-in)
- **Data Storage**: In-memory (Dict + List pattern)
- **Testing**: pytest with 100% coverage goal
- **Package Manager**: UV (fast Rust-based package manager)

## Development Principles

This project follows:
- **Spec-Driven Development (SDD)**: All code generated from specifications
- **Test-Driven Development (TDD)**: Tests written before implementation
- **Clean Code**: Simple, readable, maintainable code
- **No Over-Engineering**: Minimum viable implementation

## License

MIT License - Phase I Learning Project

## Project Evolution

This is Phase I of a 5-phase evolution:
1. **Phase I**: Console app (current)
2. **Phase II**: Full-stack web application (Next.js + FastAPI)
3. **Phase III**: AI chatbot with MCP tools
4. **Phase IV**: Local Kubernetes deployment
5. **Phase V**: Cloud deployment with Kafka & Dapr

---

**Version**: 0.1.0
**Created**: 2025-12-27
**Status**: Phase I - In Development
