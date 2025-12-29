# Fullstack Integration Skill

## Auto-Generated
- **Trigger**: Connecting Next.js frontend with FastAPI backend
- **Created**: 2025-12-29
- **Phase**: Phase 2 - Fullstack Web App
- **Reuse Count**: 0

## Purpose
Guide the integration between Next.js frontend and FastAPI backend, ensuring consistent data flow, type safety, and proper authentication handling across the stack.

## When to Use
- Connecting frontend components to backend APIs
- Setting up authentication flow
- Handling CORS issues
- Debugging frontend-backend communication
- Adding new features that span both layers

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Next.js Frontend                        │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐   │
│  │ App Router  │  │  Components  │  │    lib/api.ts     │   │
│  │  (pages)    │→→│   (React)    │→→│   (API Client)    │   │
│  └─────────────┘  └──────────────┘  └─────────┬─────────┘   │
│                                                │             │
│  ┌─────────────┐                    ┌─────────▼─────────┐   │
│  │ Better Auth │←←←←←←←←←←←←←←←←←←←│   Auth Context    │   │
│  │  (Client)   │                    │   (JWT Token)     │   │
│  └─────────────┘                    └─────────┬─────────┘   │
└───────────────────────────────────────────────┼─────────────┘
                                                │ HTTP/HTTPS
                                                ▼
┌─────────────────────────────────────────────────────────────┐
│                      FastAPI Backend                         │
│  ┌─────────────┐                    ┌───────────────────┐   │
│  │    CORS     │                    │   JWT Middleware  │   │
│  │ Middleware  │                    │   (auth.py)       │   │
│  └──────┬──────┘                    └─────────┬─────────┘   │
│         │                                     │             │
│  ┌──────▼──────────────────────────────────────▼────────┐   │
│  │                    API Routers                        │   │
│  │    (/api/{user_id}/tasks, /health)                   │   │
│  └──────────────────────────┬───────────────────────────┘   │
│                             │                               │
│  ┌──────────────────────────▼───────────────────────────┐   │
│  │                    Services Layer                     │   │
│  │              (task_service.py)                        │   │
│  └──────────────────────────┬───────────────────────────┘   │
│                             │                               │
│  ┌──────────────────────────▼───────────────────────────┐   │
│  │              SQLModel / Neon PostgreSQL              │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

## Frontend API Client Pattern

### lib/api.ts
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface FetchOptions extends RequestInit {
  token?: string;
}

async function fetchWithAuth<T>(
  endpoint: string,
  options: FetchOptions = {}
): Promise<T> {
  const { token, ...fetchOptions } = options;

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...fetchOptions,
    headers,
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(error.detail || `HTTP error: ${response.status}`);
  }

  return response.json();
}

// API methods
export const api = {
  tasks: {
    list: (userId: string, token?: string) =>
      fetchWithAuth<Task[]>(`/api/${userId}/tasks`, { token }),

    get: (userId: string, taskId: number, token?: string) =>
      fetchWithAuth<Task>(`/api/${userId}/tasks/${taskId}`, { token }),

    create: (userId: string, data: CreateTaskInput, token?: string) =>
      fetchWithAuth<Task>(`/api/${userId}/tasks`, {
        method: "POST",
        body: JSON.stringify(data),
        token,
      }),

    update: (userId: string, taskId: number, data: UpdateTaskInput, token?: string) =>
      fetchWithAuth<Task>(`/api/${userId}/tasks/${taskId}`, {
        method: "PUT",
        body: JSON.stringify(data),
        token,
      }),

    toggleComplete: (userId: string, taskId: number, token?: string) =>
      fetchWithAuth<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
        method: "PATCH",
        token,
      }),

    delete: (userId: string, taskId: number, token?: string) =>
      fetchWithAuth<void>(`/api/${userId}/tasks/${taskId}`, {
        method: "DELETE",
        token,
      }),
  },
};
```

## Type Synchronization

### Frontend Types (frontend/src/types/task.ts)
```typescript
export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string | null;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskInput {
  title: string;
  description?: string;
}

export interface UpdateTaskInput {
  title?: string;
  description?: string;
}
```

### Backend Schemas (backend/app/schemas/task.py)
```python
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

class TaskRead(BaseModel):
    id: int
    user_id: str
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

## CORS Configuration

### Backend (backend/app/main.py)
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Get from environment
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Authentication Flow

```
1. User clicks "Login" on frontend
   └─→ Better Auth handles OAuth/credentials flow

2. Better Auth creates session
   └─→ JWT token stored in cookie/localStorage

3. Frontend makes API request
   └─→ Token attached to Authorization header

4. Backend receives request
   └─→ JWT middleware validates token
   └─→ Extracts user_id from token

5. Backend checks authorization
   └─→ user_id in token matches user_id in URL

6. Request processed or rejected
```

## Common Integration Issues & Solutions

### Issue: CORS Error
```
Access to fetch at 'http://localhost:8000/api/...' from origin 'http://localhost:3000' has been blocked by CORS policy
```

**Solution**: Ensure backend CORS is configured correctly:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,  # Important for cookies
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Issue: 401 Unauthorized
**Solution**: Verify token is being sent:
```typescript
// Check token exists
const token = await getToken(); // From Better Auth
console.log("Token:", token);

// Verify header format
headers["Authorization"] = `Bearer ${token}`;
```

### Issue: Type Mismatch
**Solution**: Keep frontend types in sync with backend schemas:
```typescript
// Frontend must match backend response exactly
// Use optional chaining for nullable fields
const description = task.description ?? "No description";
```

### Issue: Network Error
**Solution**: Verify both services are running:
```bash
# Check backend
curl http://localhost:8000/health

# Check frontend
curl http://localhost:3000
```

## Environment Variables Checklist

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
BETTER_AUTH_SECRET=your-secret-min-32-chars
BETTER_AUTH_URL=http://localhost:3000
```

### Backend (.env)
```
DATABASE_URL=postgresql://user:pass@host/db?sslmode=require
BETTER_AUTH_SECRET=your-secret-min-32-chars
CORS_ORIGINS=http://localhost:3000
```

**Critical**: `BETTER_AUTH_SECRET` must be identical in both!

## Integration Testing Checklist

- [ ] Backend is running on port 8000
- [ ] Frontend is running on port 3000
- [ ] CORS allows frontend origin
- [ ] Environment variables match
- [ ] Token is sent with requests
- [ ] Types match between frontend/backend
- [ ] Error responses are handled gracefully
- [ ] Loading states show during API calls

## Quick Debug Script

```bash
#!/bin/bash
echo "=== Fullstack Integration Check ==="

# 1. Backend health
echo "1. Checking backend..."
curl -s http://localhost:8000/health && echo " [OK]" || echo " [FAIL]"

# 2. Frontend health
echo "2. Checking frontend..."
curl -s http://localhost:3000 > /dev/null && echo " [OK]" || echo " [FAIL]"

# 3. CORS preflight
echo "3. Checking CORS..."
curl -s -X OPTIONS http://localhost:8000/api/test/tasks \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: GET" \
  -I | grep -i "access-control" && echo " [OK]" || echo " [FAIL]"

echo "=== Check Complete ==="
```

---

## Version
- **Version**: 1.0.0
- **Created**: 2025-12-29
- **Category**: Fullstack Integration
- **Reuse Potential**: High (any frontend-backend connection)
