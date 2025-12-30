# MCP Tools Contract

## Overview

This document defines the contract for all MCP (Model Context Protocol) tools provided by the Todo MCP Server.

## Tool Definitions

### 1. add_task

**Description**: Create a new task with a title and optional description

**Parameters**:
```yaml
user_id:
  type: string
  required: true
  description: User ID to create task for

title:
  type: string
  required: true
  minLength: 1
  maxLength: 200
  description: Task title

description:
  type: string
  required: false
  maxLength: 1000
  description: Optional task description
```

**Returns**:
```json
{
  "id": 1,
  "user_id": "user-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T10:00:00Z"
}
```

**Error Cases**:
- Empty title: Returns validation error
- Title too long (>200 chars): Returns validation error
- Description too long (>1000 chars): Returns validation error

---

### 2. list_tasks

**Description**: List all tasks for a user with optional filtering by status

**Parameters**:
```yaml
user_id:
  type: string
  required: true
  description: User ID to list tasks for

filter:
  type: string
  required: false
  enum: ["all", "completed", "pending"]
  default: "all"
  description: Filter tasks by status
```

**Returns**:
```json
[
  {
    "id": 1,
    "user_id": "user-123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-30T10:00:00Z",
    "updated_at": "2025-12-30T10:00:00Z"
  },
  {
    "id": 2,
    "user_id": "user-123",
    "title": "Read documentation",
    "description": null,
    "completed": true,
    "created_at": "2025-12-30T09:00:00Z",
    "updated_at": "2025-12-30T11:00:00Z"
  }
]
```

**Error Cases**:
- Invalid filter: Returns validation error

---

### 3. complete_task

**Description**: Mark a task as complete or incomplete (toggle operation)

**Parameters**:
```yaml
user_id:
  type: string
  required: true
  description: User ID

task_id:
  type: integer
  required: true
  description: Task ID to mark complete/incomplete
```

**Returns**:
```json
{
  "id": 1,
  "user_id": "user-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T12:00:00Z"
}
```

**Error Cases**:
- Task not found: Returns 404 error
- User doesn't own task: Returns 403 error

---

### 4. delete_task

**Description**: Permanently delete a task

**Parameters**:
```yaml
user_id:
  type: string
  required: true
  description: User ID

task_id:
  type: integer
  required: true
  description: Task ID to delete
```

**Returns**:
```json
{
  "success": true
}
```

**Error Cases**:
- Task not found: Returns 404 error
- User doesn't own task: Returns 403 error

---

### 5. update_task

**Description**: Update task title and/or description

**Parameters**:
```yaml
user_id:
  type: string
  required: true
  description: User ID

task_id:
  type: integer
  required: true
  description: Task ID to update

title:
  type: string
  required: false
  minLength: 1
  maxLength: 200
  description: New task title

description:
  type: string
  required: false
  maxLength: 1000
  description: New task description
```

**Note**: At least one of `title` or `description` must be provided.

**Returns**:
```json
{
  "id": 1,
  "user_id": "user-123",
  "title": "Buy organic groceries",
  "description": "Milk, eggs, organic bread",
  "completed": false,
  "created_at": "2025-12-30T10:00:00Z",
  "updated_at": "2025-12-30T12:30:00Z"
}
```

**Error Cases**:
- Task not found: Returns 404 error
- User doesn't own task: Returns 403 error
- Empty title: Returns validation error
- Neither title nor description provided: Returns validation error

---

## Tool Naming Convention

All tools follow the pattern: `verb_noun` (e.g., `add_task`, `list_tasks`)

## Error Response Format

All tools return errors in the following format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Title must be between 1 and 200 characters",
    "details": {
      "field": "title",
      "value": "",
      "constraint": "minLength: 1, maxLength: 200"
    }
  }
}
```

## State Management

- **Stateless Tools**: All tools are stateless; state is persisted in the database
- **User Isolation**: All operations are scoped to a specific `user_id`
- **Transaction Safety**: Each tool operation is atomic

---

**Created**: 2025-12-30
**Version**: 1.0.0
