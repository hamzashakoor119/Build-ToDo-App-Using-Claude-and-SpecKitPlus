# Phase 2: Full-Stack Web Todo App

A modern full-stack todo application with Next.js frontend and FastAPI backend.

## Tech Stack

**Frontend:**
- Next.js 15+ (App Router)
- React 19
- TypeScript 5
- Tailwind CSS
- Better Auth (authentication)

**Backend:**
- FastAPI
- SQLModel ORM
- Neon PostgreSQL (serverless)
- JWT Authentication

## Project Structure

```
Phase_2_Fullstack_Web_App/
├── backend/
│   ├── app/
│   │   ├── main.py           # FastAPI entry point
│   │   ├── config.py         # Environment config
│   │   ├── database.py       # Database connection
│   │   ├── models/           # SQLModel definitions
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── routers/          # API endpoints
│   │   ├── services/         # Business logic
│   │   └── middleware/       # JWT verification
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js pages
│   │   ├── components/       # React components
│   │   ├── lib/              # API client, auth
│   │   └── types/            # TypeScript types
│   └── package.json
└── README.md
```

## Quick Start

### 1. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env
# Edit .env with your database credentials

# Run backend
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Create .env.local file
cp .env.example .env.local
# Edit .env.local with your settings

# Run frontend
npm run dev
```

### 3. Access the App

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://user:password@host/dbname
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
CORS_ORIGINS=http://localhost:3000
DEBUG=true
```

### Frontend (.env.local)

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
```

**Important:** `BETTER_AUTH_SECRET` must be identical in both frontend and backend.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | List all tasks |
| POST | `/api/{user_id}/tasks` | Create new task |
| GET | `/api/{user_id}/tasks/{id}` | Get single task |
| PUT | `/api/{user_id}/tasks/{id}` | Update task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task |
| GET | `/health` | Health check |

## Features

- User registration and authentication
- Create, read, update, delete tasks
- Mark tasks complete/incomplete
- Responsive design
- Real-time form validation
- Error handling with retry options

## Development Roadmap

### Current Status: Polish Phase - Final Stretch

| Phase | Status | Tasks |
|-------|--------|-------|
| Setup | Complete | T001-T009 |
| Foundation | Complete | T010-T025 |
| US1: Auth | Complete | T026-T034 |
| US2: View Tasks | Complete | T035-T043 |
| US3: Add Task | Complete | T044-T050 |
| US4: Mark Complete | Complete | T051-T056 |
| US5: Update Task | Complete | T057-T064 |
| US6: Delete Task | Complete | T065-T070 |
| Polish | **Complete** | T071-T080 |

**Progress**: 80/80 tasks complete (100%)

### Completed Polish Improvements

- **T071**: Responsive design for 320px+ mobile screens
- **T072**: Loading spinners on all async operations
- **T073**: User-friendly error messages
- **T074**: Real-time form validation with character counters
- **T075**: Created frontend/.env.local.example
- **T076**: Created backend/README.md
- **T077**: Created frontend/README.md
- **T078**: Quickstart.md validated and fixed
- **T079**: API test commands documented (specs/api-test-commands.md)
- **T080**: E2E test checklist created (specs/e2e-test-checklist.md)

See `specs/tasks.md` for the full task breakdown.

## Claude Code Integration

This project uses Claude Code for development with:

- **Skills**: Reusable patterns in `.claude/skills/`
- **Commands**: Slash commands in `.claude/commands/`
- **Specs**: Specifications in `specs/`

### Quick Commands

```bash
/status    # Get instant project status report
/summary   # Alias for /status
```

## Related Documentation

- `CLAUDE.md` - Claude Code rules and guidelines
- `specs/spec.md` - Feature specification
- `specs/plan.md` - Implementation plan
- `specs/tasks.md` - Task breakdown
