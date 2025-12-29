# Implementation Plan: Full-Stack Todo Web Application

**Branch**: `002-fullstack-web-app` | **Date**: 2025-12-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-fullstack-web/spec.md`

## Summary

Transform the Phase I console-based todo application into a modern, multi-user full-stack web application. The solution uses a monorepo architecture with Next.js 16+ frontend (App Router), FastAPI backend, SQLModel ORM, Neon Serverless PostgreSQL database, and Better Auth for JWT-based authentication. Users can register, authenticate, and perform CRUD operations on their personal todo lists through a responsive web interface.

## Technical Context

**Language/Version**:
- Frontend: TypeScript 5.x, Node.js 20+
- Backend: Python 3.13+

**Primary Dependencies**:
- Frontend: Next.js 16+, React 19, Tailwind CSS, Better Auth Client
- Backend: FastAPI, SQLModel, PyJWT, python-jose, uvicorn

**Storage**: Neon Serverless PostgreSQL (cloud-hosted)

**Testing**:
- Frontend: Jest, React Testing Library
- Backend: pytest, httpx (async testing)

**Target Platform**: Web (Desktop & Mobile browsers)

**Project Type**: Web application (frontend + backend monorepo)

**Performance Goals**:
- Task list load: < 2 seconds for 100 tasks
- API response: < 500ms for CRUD operations
- Authentication: < 1 second for login/register

**Constraints**:
- JWT token expiry: 7 days
- Task title: 1-200 characters
- Task description: max 1000 characters
- Mobile responsive: 320px minimum width

**Scale/Scope**: Single-tenant, multi-user application with 100+ concurrent users

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Gate | Status | Notes |
|------|--------|-------|
| Spec-Driven Development | PASS | spec.md created with user stories and requirements |
| Technology Stack Compliance | PASS | Using mandated stack: Next.js, FastAPI, SQLModel, Neon, Better Auth |
| Test-First Development | PENDING | Tests will be written during implementation |
| Monorepo Organization | PASS | Using frontend/ and backend/ structure |
| Clean Code Principles | PENDING | Will follow during implementation |
| PHR Creation | PASS | PHRs being created for all sessions |

## Project Structure

### Documentation (this feature)

```text
specs/002-fullstack-web/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 research output
├── data-model.md        # Phase 1 data model
├── quickstart.md        # Phase 1 quick start guide
├── contracts/           # API contracts
│   └── api-openapi.yaml # OpenAPI specification
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 task breakdown (created by /sp.tasks)
```

### Source Code (repository root)

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry
│   ├── config.py            # Configuration settings
│   ├── database.py          # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task SQLModel
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── task.py          # Pydantic schemas
│   ├── routers/
│   │   ├── __init__.py
│   │   └── tasks.py         # Task API routes
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Business logic
│   └── middleware/
│       ├── __init__.py
│       └── auth.py          # JWT verification
├── tests/
│   ├── __init__.py
│   ├── conftest.py          # Test fixtures
│   ├── test_tasks.py        # Task API tests
│   └── test_auth.py         # Auth middleware tests
├── pyproject.toml
├── requirements.txt
├── CLAUDE.md
└── .env.example

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home/redirect
│   │   ├── (auth)/
│   │   │   ├── login/
│   │   │   │   └── page.tsx
│   │   │   └── register/
│   │   │       └── page.tsx
│   │   └── dashboard/
│   │       ├── layout.tsx   # Protected layout
│   │       └── page.tsx     # Task list
│   ├── components/
│   │   ├── ui/              # Reusable UI components
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   └── Card.tsx
│   │   ├── tasks/
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskItem.tsx
│   │   │   ├── TaskForm.tsx
│   │   │   └── TaskEditModal.tsx
│   │   └── auth/
│   │       ├── LoginForm.tsx
│   │       └── RegisterForm.tsx
│   ├── lib/
│   │   ├── api.ts           # API client
│   │   ├── auth.ts          # Better Auth client
│   │   └── utils.ts         # Utility functions
│   └── types/
│       └── task.ts          # TypeScript types
├── tests/
│   └── components/
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.ts
├── CLAUDE.md
└── .env.example
```

**Structure Decision**: Web application monorepo with separate frontend and backend directories. This follows the hackathon requirement for a full-stack application with clear separation of concerns.

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                           CLIENT BROWSER                            │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FRONTEND (Next.js on Vercel)                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │   Pages     │  │ Components  │  │  API Client │                 │
│  │ (App Router)│  │ (React)     │  │  (fetch)    │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              Better Auth (Client-side Session)              │   │
│  │                    JWT Token Management                      │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                         Authorization: Bearer <JWT>
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    BACKEND (FastAPI on Cloud)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │   Routers   │  │  Services   │  │   Models    │                 │
│  │ /api/tasks  │──│ TaskService │──│  SQLModel   │                 │
│  └─────────────┘  └─────────────┘  └─────────────┘                 │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              JWT Middleware (Verify Token)                   │   │
│  │           Validates user_id matches token                    │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    DATABASE (Neon PostgreSQL)                       │
│  ┌─────────────────────┐  ┌─────────────────────┐                  │
│  │       users         │  │       tasks         │                  │
│  │ (Better Auth)       │  │ (SQLModel)          │                  │
│  └─────────────────────┘  └─────────────────────┘                  │
└─────────────────────────────────────────────────────────────────────┘
```

## Authentication Flow

```
1. User registers/logs in via Better Auth on Frontend
2. Better Auth creates session and issues JWT token
3. Frontend stores JWT token securely
4. For each API request, Frontend includes: Authorization: Bearer <token>
5. Backend middleware extracts and verifies JWT
6. Backend validates user_id in URL matches token's user_id
7. Backend returns only that user's data
```

## Implementation Phases

### Phase 1: Backend Foundation
1. Set up FastAPI project structure
2. Configure Neon PostgreSQL connection
3. Create Task SQLModel with migrations
4. Implement JWT verification middleware
5. Create task CRUD endpoints

### Phase 2: Frontend Foundation
1. Set up Next.js 16+ project with App Router
2. Configure Better Auth client
3. Create authentication pages (login, register)
4. Set up protected routes

### Phase 3: Task Management UI
1. Create task list component
2. Implement add task functionality
3. Implement edit task modal
4. Implement delete with confirmation
5. Implement completion toggle

### Phase 4: Integration & Testing
1. Connect frontend API client to backend
2. Write backend API tests
3. Write frontend component tests
4. End-to-end testing

### Phase 5: Deployment
1. Deploy backend (Railway/Render/Fly.io)
2. Deploy frontend to Vercel
3. Configure environment variables
4. Test production deployment

## Key Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| State Management | React hooks + fetch | Simple enough for CRUD, no Redux needed |
| API Client | Native fetch | Built-in, no extra dependency |
| CSS Framework | Tailwind CSS | Rapid development, responsive utilities |
| Form Handling | React Hook Form | Validation, performance |
| Backend Hosting | Railway/Render | Easy Python deployment, free tier |
| Database | Neon PostgreSQL | Serverless, free tier, easy setup |

## Complexity Tracking

No constitution violations requiring justification. The architecture follows the mandated technology stack and monorepo structure specified in the hackathon requirements.

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Better Auth + FastAPI JWT integration complexity | Medium | High | Research and document integration pattern |
| CORS issues between frontend and backend | Medium | Medium | Configure proper CORS headers |
| Neon cold starts affecting performance | Low | Medium | Connection pooling, keep-alive |
| Vercel timeout for API calls | Low | Medium | Optimize backend response times |

## Dependencies

| Dependency | Version | Purpose |
|------------|---------|---------|
| Next.js | 16+ | Frontend framework |
| React | 19+ | UI library |
| Tailwind CSS | 3.x | Styling |
| Better Auth | Latest | Authentication |
| FastAPI | 0.100+ | Backend framework |
| SQLModel | 0.0.16+ | ORM |
| PyJWT | 2.x | JWT handling |
| Neon | - | PostgreSQL hosting |

## Success Metrics

Aligned with spec.md Success Criteria:
- SC-001: Registration < 30 seconds
- SC-002: Add task < 5 seconds
- SC-003: Task list load < 2 seconds (100 tasks)
- SC-004: All 5 CRUD operations functional
- SC-005: 100% user data isolation
- SC-006: Mobile responsive (320px+)
- SC-007: Graceful error handling
- SC-008: Data persistence across sessions
