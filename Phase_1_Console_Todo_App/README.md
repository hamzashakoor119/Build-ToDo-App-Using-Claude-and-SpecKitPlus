# Phase 1: Console Todo App

A simple, interactive command-line todo application built with Python using Spec-Driven Development.

## Features

- **Add Task** - Create new tasks with title and optional description
- **View Tasks** - List all tasks with status indicators
- **Update Task** - Modify task title or description
- **Delete Task** - Remove tasks permanently
- **Mark Complete/Incomplete** - Toggle task completion status
- **Dual Mode** - Interactive menu OR command-line arguments
- **In-Memory Storage** - Fast operations (data cleared on exit)

## Requirements

- Python 3.13+
- UV package manager (recommended) or pip

## Quick Start

### Installation

```bash
# Navigate to project directory
cd Phase_1_Console_Todo_App

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv sync

# Install in development mode
uv pip install -e .
```

### Running the App

#### Interactive Mode (Menu-Driven)

```bash
# Option 1: Run directly
python main.py

# Option 2: Run as module
python -m todo_app

# Option 3: Use installed command
todo
```

#### Command-Line Mode

```bash
# Add a task
python -m todo_app add "Buy groceries"
python -m todo_app add "Call mom" --description "Discuss weekend plans"

# List all tasks
python -m todo_app list

# Mark task complete (use first 8 chars of ID)
python -m todo_app complete abc12345

# Mark task incomplete
python -m todo_app incomplete abc12345

# Update task
python -m todo_app update abc12345 "Buy organic groceries"

# Delete task
python -m todo_app delete abc12345

# Get help
python -m todo_app --help
python -m todo_app add --help
```

## Running Tests

```bash
# Run all tests with coverage
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_models.py

# Run with coverage report
uv run pytest --cov=todo_app --cov-report=html
```

## Project Structure

```
Phase_1_Console_Todo_App/
├── main.py                 # Entry point (interactive mode)
├── pyproject.toml          # Project configuration
├── README.md               # This file
├── CLAUDE.md               # Claude Code instructions
│
├── src/
│   └── todo_app/
│       ├── __init__.py     # Package initialization
│       ├── __main__.py     # Module entry point (dual mode)
│       ├── main.py         # Main entry point
│       ├── cli.py          # CLI argument parser & commands
│       ├── interactive.py  # Interactive menu interface
│       ├── models.py       # Task data model
│       └── storage.py      # In-memory task storage
│
├── tests/
│   ├── __init__.py
│   ├── test_models.py      # Task model tests
│   ├── test_storage.py     # Storage operation tests
│   └── test_cli.py         # CLI integration tests
│
├── specs/                  # Specification documents
│   ├── spec.md             # Feature specification
│   ├── plan.md             # Implementation plan
│   ├── tasks.md            # Task breakdown
│   ├── data-model.md       # Data model specification
│   ├── research.md         # Technical research
│   ├── quickstart.md       # Quick start guide
│   ├── contracts/          # Interface contracts
│   └── checklists/         # Requirements checklists
│
├── history/
│   └── prompts/            # Prompt History Records (PHRs)
│
└── .specify/
    ├── memory/
    │   └── constitution.md # Project constitution
    └── templates/          # Spec-Kit templates
```

## Usage Examples

### Interactive Mode

```
$ python main.py

🎯 Welcome to Todo Application!

==================================================
           TODO APPLICATION
==================================================

[1] ➕ Add Task
[2] 📋 List Tasks
[3] ✅ Mark Complete
[4] ⭕ Mark Incomplete
[5] ✏️  Update Task
[6] 🗑️  Delete Task
[7] 🚪 Exit
--------------------------------------------------
Select option (1-7): 1

Enter task title: Buy groceries
Enter description (optional): Milk, eggs, bread

✓ Task added successfully!
ID: a1b2c3d4
Title: Buy groceries
Description: Milk, eggs, bread
```

### CLI Mode

```bash
$ python -m todo_app add "Complete Phase 1" --description "Fix all gaps"
✓ Task added successfully
ID: e5f6g7h8
Title: Complete Phase 1
Description: Fix all gaps

$ python -m todo_app list
Tasks (1):

  [○] e5f6g7h8... Complete Phase 1

$ python -m todo_app complete e5f6g7h8
✓ Task marked as complete
ID: e5f6g7h8
Title: Complete Phase 1
```

## Storage

**In-Memory Storage**: All tasks are stored in memory during the application session. When the application exits, all data is cleared. This is by design for Phase 1 - persistent storage is added in Phase 2.

### Data Model

```python
Task:
    id: str           # UUID v4 (auto-generated)
    title: str        # 1-200 characters
    description: str  # Optional, up to 1000 characters
    completed: bool   # Default: False
    created_at: str   # ISO 8601 timestamp
```

## Spec-Driven Development

This project follows **Spec-Driven Development** using Claude Code and Spec-Kit Plus:

1. **Constitution** - Project principles in `.specify/memory/constitution.md`
2. **Specification** - Feature requirements in `specs/spec.md`
3. **Plan** - Implementation plan in `specs/plan.md`
4. **Tasks** - Task breakdown in `specs/tasks.md`
5. **PHRs** - Development history in `history/prompts/`

## Phase 1 Scope

### Included (Basic Level)
- Add task with title and description
- Delete task by ID
- Update task details
- View all tasks with status
- Mark task complete/incomplete
- Interactive CLI mode
- Command-line argument mode

### Not Included (Future Phases)
- Persistent storage (Phase 2)
- User authentication (Phase 2)
- Web interface (Phase 2)
- AI Chatbot (Phase 3)
- Kubernetes deployment (Phase 4-5)

## License

This project is part of the GIAIC Hackathon II - Spec-Driven Development.

---

**Phase**: 1 of 5 - In-Memory Python Console App
**Technology**: Python 3.13+, UV, pytest
**Status**: Complete
