# Phase 2 Backend - FastAPI Todo API

A RESTful API for the Todo application built with FastAPI, SQLModel, and Neon PostgreSQL.

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLModel (SQLAlchemy + Pydantic)
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: JWT verification (tokens from Better Auth)
- **Python**: 3.11+

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI app entry point
│   ├── config.py         # Environment configuration
│   ├── database.py       # Database connection
│   ├── models/           # SQLModel database models
│   │   ├── __init__.py
│   │   └── task.py       # Task model
│   ├── schemas/          # Pydantic request/response schemas
│   │   ├── __init__.py
│   │   └── task.py       # Task schemas
│   ├── routers/          # API route handlers
│   │   ├── __init__.py
│   │   └── tasks.py      # Task CRUD endpoints
│   ├── services/         # Business logic
│   │   ├── __init__.py
│   │   └── task_service.py
│   └── middleware/       # Custom middleware
│       ├── __init__.py
│       └── auth.py       # JWT verification
├── tests/                # Test files
├── .env.example          # Environment template
├── pyproject.toml        # Python project config
└── requirements.txt      # Dependencies
```

## Quick Start

### Prerequisites

- Python 3.11 or higher
- A Neon PostgreSQL database (free tier available at [neon.tech](https://neon.tech))

### 1. Create Virtual Environment

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate it
# On Linux/macOS:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your values
```

Required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| `DATABASE_URL` | Neon PostgreSQL connection string | `postgresql+asyncpg://user:pass@host/db?sslmode=require` |
| `BETTER_AUTH_SECRET` | JWT secret (must match frontend) | `your-32-char-secret-key` |
| `CORS_ORIGINS` | Allowed frontend origins | `http://localhost:3000` |
| `DEBUG` | Enable debug mode | `true` |

### 4. Run the Server

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload --port 8000

# Production mode
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 5. Verify It's Running

- API Root: http://localhost:8000
- Health Check: http://localhost:8000/health
- API Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Health Check

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Server health status |

### Task Operations

All task endpoints require JWT authentication and are scoped to the authenticated user.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks for user |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get a specific task |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |

### Request/Response Examples

#### Create Task

```bash
curl -X POST "http://localhost:8000/api/user123/tasks" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}'
```

Response:
```json
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-29T12:00:00Z",
  "updated_at": "2025-12-29T12:00:00Z"
}
```

#### Toggle Complete

```bash
curl -X PATCH "http://localhost:8000/api/user123/tasks/1/complete" \
  -H "Authorization: Bearer <token>"
```

## Database Setup

The database tables are created automatically on first run. The Task model includes:

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer | Primary key (auto-increment) |
| `user_id` | String | Owner's user ID |
| `title` | String(200) | Task title (required) |
| `description` | String(1000) | Optional description |
| `completed` | Boolean | Completion status |
| `created_at` | DateTime | Creation timestamp |
| `updated_at` | DateTime | Last update timestamp |

## Development

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app
```

### Code Style

```bash
# Format code
black app/

# Sort imports
isort app/

# Type checking
mypy app/
```

## Troubleshooting

### Common Issues

**Connection refused on port 8000**
- Ensure no other service is using port 8000
- Try: `lsof -i :8000` to check

**Database connection failed**
- Verify DATABASE_URL is correct
- Ensure `?sslmode=require` is included for Neon
- Check if your IP is allowlisted in Neon dashboard

**CORS errors**
- Verify CORS_ORIGINS includes your frontend URL
- Check for trailing slashes (should not have them)

**JWT validation failed**
- Ensure BETTER_AUTH_SECRET matches the frontend exactly
- Check token format: `Bearer <token>`

## Related

- [Frontend README](../frontend/README.md)
- [Main Project README](../README.md)
- [API Specification](../specs/spec.md)
