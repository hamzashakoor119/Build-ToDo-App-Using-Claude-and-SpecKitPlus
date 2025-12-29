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
