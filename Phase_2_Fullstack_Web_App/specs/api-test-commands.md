# API Endpoint Testing Commands

**Purpose**: Verify all 6 task endpoints work correctly per API contract.
**Prerequisites**: Backend running on `http://localhost:8000`

## Test Setup

You'll need a valid JWT token for testing. For development testing, you can:
1. Start the backend and frontend
2. Register/Login through the UI
3. Copy the token from browser dev tools (Network tab, Authorization header)

Or create a test token manually using the same BETTER_AUTH_SECRET.

```bash
# Set variables for testing
export API_URL="http://localhost:8000"
export USER_ID="test-user-123"
export TOKEN="your-jwt-token-here"
```

## 1. Health Check (No Auth Required)

```bash
curl -X GET "${API_URL}/health"
```

**Expected Response (200 OK)**:
```json
{"status": "healthy", "cors": "enabled"}
```

---

## 2. List Tasks - GET /api/{user_id}/tasks

```bash
curl -X GET "${API_URL}/api/${USER_ID}/tasks" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json"
```

**Expected Response (200 OK)** - Empty list or list of tasks:
```json
[]
```

or

```json
[
  {
    "id": 1,
    "user_id": "test-user-123",
    "title": "Sample Task",
    "description": "Task description",
    "completed": false,
    "created_at": "2025-12-29T12:00:00Z",
    "updated_at": "2025-12-29T12:00:00Z"
  }
]
```

---

## 3. Create Task - POST /api/{user_id}/tasks

```bash
curl -X POST "${API_URL}/api/${USER_ID}/tasks" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "description": "Testing the API"}'
```

**Expected Response (201 Created)**:
```json
{
  "id": 1,
  "user_id": "test-user-123",
  "title": "Test Task",
  "description": "Testing the API",
  "completed": false,
  "created_at": "2025-12-29T12:00:00Z",
  "updated_at": "2025-12-29T12:00:00Z"
}
```

### Validation Test - Empty Title

```bash
curl -X POST "${API_URL}/api/${USER_ID}/tasks" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"title": "", "description": "No title"}'
```

**Expected Response (422 Unprocessable Entity)**:
```json
{
  "detail": [{"loc": ["body", "title"], "msg": "...", "type": "..."}]
}
```

---

## 4. Get Single Task - GET /api/{user_id}/tasks/{task_id}

```bash
curl -X GET "${API_URL}/api/${USER_ID}/tasks/1" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json"
```

**Expected Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": "test-user-123",
  "title": "Test Task",
  "description": "Testing the API",
  "completed": false,
  "created_at": "2025-12-29T12:00:00Z",
  "updated_at": "2025-12-29T12:00:00Z"
}
```

### Not Found Test

```bash
curl -X GET "${API_URL}/api/${USER_ID}/tasks/99999" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json"
```

**Expected Response (404 Not Found)**:
```json
{"detail": "Task not found"}
```

---

## 5. Update Task - PUT /api/{user_id}/tasks/{task_id}

```bash
curl -X PUT "${API_URL}/api/${USER_ID}/tasks/1" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated Title", "description": "Updated description"}'
```

**Expected Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": "test-user-123",
  "title": "Updated Title",
  "description": "Updated description",
  "completed": false,
  "created_at": "2025-12-29T12:00:00Z",
  "updated_at": "2025-12-29T12:05:00Z"
}
```

---

## 6. Toggle Complete - PATCH /api/{user_id}/tasks/{task_id}/complete

```bash
curl -X PATCH "${API_URL}/api/${USER_ID}/tasks/1/complete" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json"
```

**Expected Response (200 OK)** - First call sets completed=true:
```json
{
  "id": 1,
  "user_id": "test-user-123",
  "title": "Updated Title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2025-12-29T12:00:00Z",
  "updated_at": "2025-12-29T12:06:00Z"
}
```

**Second call** sets completed=false (toggle behavior).

---

## 7. Delete Task - DELETE /api/{user_id}/tasks/{task_id}

```bash
curl -X DELETE "${API_URL}/api/${USER_ID}/tasks/1" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -v
```

**Expected Response (204 No Content)** - No body, just status code.

### Verify Deletion

```bash
curl -X GET "${API_URL}/api/${USER_ID}/tasks/1" \
  -H "Authorization: Bearer ${TOKEN}"
```

**Expected Response (404 Not Found)**:
```json
{"detail": "Task not found"}
```

---

## Authentication Tests

### No Token (401 Unauthorized)

```bash
curl -X GET "${API_URL}/api/${USER_ID}/tasks"
```

**Expected Response (401)**:
```json
{"detail": "Not authenticated"}
```

### Invalid Token (401 Unauthorized)

```bash
curl -X GET "${API_URL}/api/${USER_ID}/tasks" \
  -H "Authorization: Bearer invalid-token"
```

**Expected Response (401)**:
```json
{"detail": "Invalid token"}
```

### Wrong User ID (403 Forbidden)

```bash
curl -X GET "${API_URL}/api/other-user/tasks" \
  -H "Authorization: Bearer ${TOKEN}"
```

**Expected Response (403)**:
```json
{"detail": "Access denied"}
```

---

## Full Test Sequence

Run this sequence to test the complete CRUD flow:

```bash
# 1. Health check
curl -s "${API_URL}/health" | jq .

# 2. Create a task
TASK=$(curl -s -X POST "${API_URL}/api/${USER_ID}/tasks" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries", "description": "Milk, eggs, bread"}')
echo "Created: $TASK"
TASK_ID=$(echo $TASK | jq -r '.id')

# 3. List tasks
curl -s "${API_URL}/api/${USER_ID}/tasks" \
  -H "Authorization: Bearer ${TOKEN}" | jq .

# 4. Get single task
curl -s "${API_URL}/api/${USER_ID}/tasks/${TASK_ID}" \
  -H "Authorization: Bearer ${TOKEN}" | jq .

# 5. Update task
curl -s -X PUT "${API_URL}/api/${USER_ID}/tasks/${TASK_ID}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries (updated)", "description": "Milk, eggs, bread, butter"}' | jq .

# 6. Toggle complete
curl -s -X PATCH "${API_URL}/api/${USER_ID}/tasks/${TASK_ID}/complete" \
  -H "Authorization: Bearer ${TOKEN}" | jq .

# 7. Delete task
curl -s -X DELETE "${API_URL}/api/${USER_ID}/tasks/${TASK_ID}" \
  -H "Authorization: Bearer ${TOKEN}" -w "\nStatus: %{http_code}\n"

# 8. Verify deletion
curl -s "${API_URL}/api/${USER_ID}/tasks/${TASK_ID}" \
  -H "Authorization: Bearer ${TOKEN}" | jq .
```

---

## Test Checklist

| Endpoint | Method | Auth | Status | Notes |
|----------|--------|------|--------|-------|
| /health | GET | No | ✅ | Returns healthy status |
| /api/{user_id}/tasks | GET | Yes | ✅ | List all user tasks |
| /api/{user_id}/tasks | POST | Yes | ✅ | Create new task |
| /api/{user_id}/tasks/{id} | GET | Yes | ✅ | Get single task |
| /api/{user_id}/tasks/{id} | PUT | Yes | ✅ | Update task |
| /api/{user_id}/tasks/{id}/complete | PATCH | Yes | ✅ | Toggle completion |
| /api/{user_id}/tasks/{id} | DELETE | Yes | ✅ | Delete task |

All 6 task endpoints + health check verified against API contract.
