# Todo MCP Server

Model Context Protocol (MCP) server providing 5 tools for task management.

## Tools

1. `add_task` - Create a new task
2. `list_tasks` - List all user's tasks
3. `complete_task` - Mark task as complete/incomplete
4. `delete_task` - Delete a task
5. `update_task` - Update task details

## Setup

1. Create a `.env` file:
```
BACKEND_URL=http://localhost:8000
```

2. Install dependencies:
```bash
uv sync
```

3. Run the server:
```bash
uv run python server.py
```

## MCP Server Configuration

Add to your MCP client configuration:

```json
{
  "mcpServers": {
    "todo": {
      "command": "uv",
      "args": ["run", "python", "/path/to/Phase_3/mcp-server/server.py"],
      "env": {
        "BACKEND_URL": "http://localhost:8000"
      }
    }
  }
}
```
