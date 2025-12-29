# Phase 2 Constitution: Fullstack Web App

## Project Overview

**Phase**: 2 - Full-Stack Web Application
**Purpose**: Build a complete web-based Todo application with authentication
**Technology**: Next.js + FastAPI + Neon PostgreSQL

## Core Principles

### I. Spec-Driven Development (MANDATORY)
- All code must be generated from specifications
- Specifications in `/specs` directory
- No manual coding without spec

### II. Test-First Development
- Write tests before implementation
- Frontend: Jest + React Testing Library
- Backend: pytest
- All tests must pass

### III. Monorepo Organization
- `/frontend` for Next.js application
- `/backend` for FastAPI application
- Shared specs and history at root

## Technology Stack

### Frontend
| Component | Technology |
|-----------|------------|
| Framework | Next.js 16+ (App Router) |
| Language | TypeScript |
| Styling | Tailwind CSS |
| Auth | Better Auth Client |

### Backend
| Component | Technology |
|-----------|------------|
| Framework | FastAPI |
| ORM | SQLModel |
| Database | Neon PostgreSQL |
| Auth | Better Auth + JWT |

## Features Scope

### In Scope
- All Basic Level features (CRUD)
- User authentication (register, login, logout)
- Session management (JWT)
- User-specific task isolation
- Responsive web UI

### Out of Scope
- AI integration
- Real-time updates
- File attachments
- Kubernetes deployment

## API Standards

- RESTful conventions
- JSON request/response
- HTTP status codes for errors
- Input validation (Pydantic)
- JWT in Authorization header

## Database Standards

- SQLModel for all operations
- Proper foreign keys (user_id on tasks)
- Environment-based connection strings
- Connection pooling

## Quality Standards

- Code coverage > 70%
- No security vulnerabilities (XSS, SQL injection)
- Proper error handling
- Type safety (TypeScript/Pydantic)

## Success Criteria

- [ ] Responsive web UI
- [ ] RESTful API working
- [ ] Authentication functional
- [ ] JWT verification
- [ ] Database integrated
- [ ] All tests passing
- [ ] Documentation complete

---
**Version**: 1.0.0
**Phase**: 2 of 5
**Ratified**: 2025-12-29
