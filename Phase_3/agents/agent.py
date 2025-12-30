"""
OpenAI Agents SDK Integration for Todo Assistant

This module provides the AI agent that manages conversations
and calls MCP tools for task operations.
"""

import os
from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class AgentConfig:
    """Configuration for the Todo Assistant agent."""
    name: str = "Todo Assistant"
    description: str = "AI-powered todo task management assistant"
    instructions: str = (
        "You are a helpful assistant that helps users manage their todo tasks. "
        "Use the available MCP tools to perform task operations. "
        "Always confirm the action before executing it."
    )
    model: str = "gpt-4o-mini"
    temperature: float = 0.7
    domain_allowlist: list = None

    def __post_init__(self):
        if self.domain_allowlist is None:
            self.domain_allowlist = ["openai.com"]


class TodoAgent:
    """Main AI agent for todo task management."""

    def __init__(self, config: Optional[AgentConfig] = None):
        """Initialize the Todo Agent."""
        self.config = config or AgentConfig()
        self.mcp_server_url = os.getenv("MCP_SERVER_URL", "http://localhost:3001")
        self.api_key = os.getenv("OPENAI_API_KEY")

        if not self.api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")

    def get_config(self) -> Dict[str, Any]:
        """Get agent configuration as dictionary."""
        return {
            "name": self.config.name,
            "description": self.config.description,
            "instructions": self.config.instructions,
            "model": self.config.model,
            "temperature": self.config.temperature,
            "domain": {
                "allowlist": self.config.domain_allowlist
            },
            "mcp_server": {
                "name": "todo-server",
                "url": self.mcp_server_url
            }
        }

    async def process_message(self, user_id: str, message: str) -> str:
        """
        Process a user message and generate a response.

        Args:
            user_id: The user's ID for task operations
            message: The user's message

        Returns:
            The agent's response
        """
        # TODO: Implement with OpenAI Agents SDK
        # This will integrate with MCP Server and OpenAI API

        return "OpenAI Agents SDK integration coming soon!"


def create_agent() -> TodoAgent:
    """Factory function to create a configured Todo Agent."""
    return TodoAgent()


if __name__ == "__main__":
    import asyncio
    import json

    agent = create_agent()
    print("Agent Configuration:")
    print(json.dumps(agent.get_config(), indent=2))
