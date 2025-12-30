"""MCP Server for Todo Application with 5 tools for task management."""

import os
from typing import Any, Optional

import httpx
from mcp.server import Server
from mcp.types import (
    Resource,
    Tool,
    TextContent,
    ImageContent,
    EmbeddedResource,
)

# Initialize MCP server
server = Server("todo-server")

# Backend API URL from environment
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


async def call_backend(method: str, endpoint: str, user_id: str, data: Optional[dict] = None) -> Any:
    """Call the Phase 2 FastAPI backend."""
    async with httpx.AsyncClient() as client:
        url = f"{BACKEND_URL}{endpoint}"
        headers = {}

        if method == "GET":
            response = await client.get(url, headers=headers)
        elif method == "POST":
            response = await client.post(url, json=data, headers=headers)
        elif method == "PUT":
            response = await client.put(url, json=data, headers=headers)
        elif method == "PATCH":
            response = await client.patch(url, headers=headers)
        elif method == "DELETE":
            response = await client.delete(url, headers=headers)
        else:
            raise ValueError(f"Unsupported method: {method}")

        response.raise_for_status()

        if method == "DELETE":
            return {"success": True}

        return response.json()


@server.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="todo://tasks",
            name="Tasks",
            description="User's todo tasks",
            mimeType="application/json",
        )
    ]


@server.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools."""
    return [
        Tool(
            name="add_task",
            description="Create a new task with a title and optional description",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID to create task for",
                    },
                    "title": {
                        "type": "string",
                        "description": "Task title (1-200 characters)",
                        "minLength": 1,
                        "maxLength": 200,
                    },
                    "description": {
                        "type": "string",
                        "description": "Optional task description (max 1000 characters)",
                        "maxLength": 1000,
                    },
                },
                "required": ["user_id", "title"],
            },
        ),
        Tool(
            name="list_tasks",
            description="List all tasks for a user with optional filtering",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID to list tasks for",
                    },
                    "filter": {
                        "type": "string",
                        "description": "Filter tasks by status: 'all', 'completed', or 'pending'",
                        "enum": ["all", "completed", "pending"],
                        "default": "all",
                    },
                },
                "required": ["user_id"],
            },
        ),
        Tool(
            name="complete_task",
            description="Mark a task as complete or incomplete",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID",
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to mark complete/incomplete",
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
        Tool(
            name="delete_task",
            description="Permanently delete a task",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID",
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to delete",
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
        Tool(
            name="update_task",
            description="Update task title and/or description",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {
                        "type": "string",
                        "description": "User ID",
                    },
                    "task_id": {
                        "type": "integer",
                        "description": "Task ID to update",
                    },
                    "title": {
                        "type": "string",
                        "description": "New task title (1-200 characters)",
                        "minLength": 1,
                        "maxLength": 200,
                    },
                    "description": {
                        "type": "string",
                        "description": "New task description (max 1000 characters)",
                        "maxLength": 1000,
                    },
                },
                "required": ["user_id", "task_id"],
            },
        ),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent | ImageContent | EmbeddedResource]:
    """Handle tool calls."""

    try:
        if name == "add_task":
            user_id = arguments["user_id"]
            title = arguments["title"]
            description = arguments.get("description")

            result = await call_backend(
                "POST",
                f"/api/{user_id}/tasks",
                user_id,
                {"title": title, "description": description},
            )

            status_icon = "✓" if result["completed"] else "○"
            return [
                TextContent(
                    type="text",
                    text=f"Task created successfully!\n\n"
                    f"[{status_icon}] #{result['id']} {result['title']}\n"
                    f"Description: {result['description'] or 'None'}\n"
                    f"Status: {'Completed' if result['completed'] else 'Pending'}",
                )
            ]

        elif name == "list_tasks":
            user_id = arguments["user_id"]
            filter_type = arguments.get("filter", "all")

            tasks = await call_backend("GET", f"/api/{user_id}/tasks", user_id)

            # Filter tasks if needed
            if filter_type == "completed":
                tasks = [t for t in tasks if t["completed"]]
            elif filter_type == "pending":
                tasks = [t for t in tasks if not t["completed"]]

            if not tasks:
                return [
                    TextContent(
                        type="text",
                        text=f"No {'completed' if filter_type == 'completed' else 'pending' if filter_type == 'pending' else ''} tasks found.",
                    )
                ]

            # Format task list
            output_lines = [f"Your Tasks ({len(tasks)} total):", ""]
            for task in tasks:
                status_icon = "✓" if task["completed"] else "○"
                output_lines.append(
                    f"[{status_icon}] #{task['id']} {task['title']}"
                )
                if task.get("description"):
                    output_lines.append(f"    {task['description']}")

            return [TextContent(type="text", text="\n".join(output_lines))]

        elif name == "complete_task":
            user_id = arguments["user_id"]
            task_id = arguments["task_id"]

            result = await call_backend(
                "PATCH", f"/api/{user_id}/tasks/{task_id}/complete", user_id
            )

            status_icon = "✓" if result["completed"] else "○"
            status_text = "Completed" if result["completed"] else "Pending"

            return [
                TextContent(
                    type="text",
                    text=f"Task status updated!\n\n"
                    f"[{status_icon}] #{result['id']} {result['title']}\n"
                    f"Status: {status_text}",
                )
            ]

        elif name == "delete_task":
            user_id = arguments["user_id"]
            task_id = arguments["task_id"]

            await call_backend("DELETE", f"/api/{user_id}/tasks/{task_id}", user_id)

            return [
                TextContent(
                    type="text",
                    text=f"Task #{task_id} deleted successfully.",
                )
            ]

        elif name == "update_task":
            user_id = arguments["user_id"]
            task_id = arguments["task_id"]
            title = arguments.get("title")
            description = arguments.get("description")

            # Build update data with only provided fields
            update_data = {}
            if title is not None:
                update_data["title"] = title
            if description is not None:
                update_data["description"] = description

            result = await call_backend(
                "PUT", f"/api/{user_id}/tasks/{task_id}", user_id, update_data
            )

            status_icon = "✓" if result["completed"] else "○"

            return [
                TextContent(
                    type="text",
                    text=f"Task updated successfully!\n\n"
                    f"[{status_icon}] #{result['id']} {result['title']}\n"
                    f"Description: {result['description'] or 'None'}\n"
                    f"Status: {'Completed' if result['completed'] else 'Pending'}",
                )
            ]

        else:
            return [
                TextContent(
                    type="text",
                    text=f"Unknown tool: {name}",
                )
            ]

    except httpx.HTTPStatusError as e:
        error_msg = f"Error calling backend: {e.response.status_code}"
        try:
            error_data = e.response.json()
            if "detail" in error_data:
                error_msg = f"Error: {error_data['detail']}"
        except:
            pass
        return [TextContent(type="text", text=error_msg)]

    except Exception as e:
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server

    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
