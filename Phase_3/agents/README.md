# OpenAI Agents Configuration

Configuration for the Todo Assistant AI agent using OpenAI Agents SDK.

## Setup

1. Install dependencies:
```bash
npm install @ai-sdk/openai ai
```

2. Set environment variables:
```
OPENAI_API_KEY=sk-your-openai-api-key
```

## Agent Configuration

The agent is configured in `config.json` with:

- **Model**: GPT-4o-mini
- **Temperature**: 0.7 (balanced creativity)
- **Domain**: openai.com (security restriction)
- **Tools**: 5 MCP tools for task management

## Tool Bindings

The agent is configured to use the following MCP tools:

1. `add_task` - Create new tasks
2. `list_tasks` - List user's tasks
3. `complete_task` - Mark tasks as complete
4. `delete_task` - Delete tasks
5. `update_task` - Update task details

## Future Implementation

This configuration will be used with OpenAI Agents SDK to provide:
- Natural language understanding
- Context awareness across conversations
- Multi-turn conversations
- Intent detection and disambiguation
