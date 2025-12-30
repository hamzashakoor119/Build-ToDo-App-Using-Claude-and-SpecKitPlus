# Phase 3: AI-Powered Todo Chatbot

Transform web-based todo application into an AI-powered chatbot that allows users to manage tasks through natural language.

## Overview

Phase 3 adds a conversational interface on top of Phase 2's full-stack web application, enabling users to interact with their todo list using natural language commands.

## Status

**Phase Status**: COMPLETE ✅

## Technology Stack

| Component | Technology | Version |
|-----------|-------------|----------|
| Chat UI | Next.js | 15.0.3 |
|  | React | 19.0.0 |
|  | TypeScript | 5.0.0 |
|  | Tailwind CSS | 3.4.0 |
| MCP Server | Python | 3.13+ |
|  | MCP SDK | 1.0.0 |
|  | httpx | 0.24.0 |
| AI Agent | OpenAI GPT-4o-mini | Latest |
| Backend | FastAPI (Phase 2) | 0.100.0+ |
| Database | Neon PostgreSQL | Serverless |

## Features

Manage tasks via natural language:
- **Add Task**: "Add a task to buy groceries"
- **View Tasks**: "Show my tasks" / "Show completed tasks" / "Show pending tasks"
- **Complete Task**: "Mark task #1 as done"
- **Delete Task**: "Delete task #3"
- **Update Task**: "Update task #1 title to 'Buy organic groceries'"

## Architecture

```
User Input (Natural Language)
    ↓
ChatKit UI (React/Next.js)
    ↓
OpenAI Agents SDK (NLP Processing)
    ↓
MCP Server (Tool Orchestration)
    ↓
FastAPI Backend (Phase 2)
    ↓
Neon PostgreSQL Database
```

## Project Structure

```
Phase_3/
├── .claude/              # Claude Code configuration
├── .specify/             # SpecKit Plus configuration
├── specs/                # Feature specifications
│   ├── contracts/         # MCP tool contracts
│   │   └── mcp-tools.md
│   ├── spec.md
│   └── checklists/
├── history/              # Development history
├── chatbot/              # ChatKit UI
│   ├── src/
│   │   ├── app/         # Next.js pages
│   │   ├── components/   # React components
│   │   │   └── chat/   # Chat UI components
│   │   ├── lib/         # AI agent logic
│   │   └── types/      # TypeScript types
│   ├── package.json
│   ├── .env.example
│   └── README.md
├── mcp-server/           # MCP Server
│   ├── server.py         # Main server with 5 tools
│   ├── pyproject.toml    # Python dependencies
│   ├── .env.example
│   └── README.md
├── agents/               # OpenAI Agents config
│   ├── config.json       # Agent configuration
│   ├── agent.py         # Python agent wrapper
│   └── README.md
└── README.md            # This file
```

## Getting Started

### Prerequisites

1. **Phase 2 Backend** must be running:
```bash
cd ../Phase_2_Fullstack_Web_App/backend
uv run uvicorn app.main:app --reload
```

2. **OpenAI API Key** required

### ChatBot UI Setup

```bash
cd chatbot
npm install
cp .env.example .env.local
# Edit .env.local with your API keys
npm run dev
```

### MCP Server Setup

```bash
cd mcp-server
uv sync
cp .env.example .env
# Edit .env with backend URL
uv run python server.py
```

## Environment Variables

### ChatBot (.env.local)

```env
OPENAI_API_KEY=sk-your-openai-api-key
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_MCP_SERVER_URL=http://localhost:3001
BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your-secret-key-min-32-chars
NEXT_PUBLIC_ALLOWED_DOMAINS=openai.com
```

### MCP Server (.env)

```env
BACKEND_URL=http://localhost:8000
```

## Running the Application

1. Start Phase 2 Backend (Port 8000)
2. Start MCP Server (Port 3001) - *Optional for demo*
3. Start ChatBot UI (Port 3000)
4. Open http://localhost:3000
5. Enter a user ID and start chatting!

## MCP Tools Contract

See `specs/contracts/mcp-tools.md` for detailed documentation of all 5 MCP tools:

1. `add_task` - Create new tasks
2. `list_tasks` - List user's tasks (with filtering)
3. `complete_task` - Toggle task completion
4. `delete_task` - Delete tasks
5. `update_task` - Update task details

## Implementation Status

- [x] ChatKit UI implemented
- [x] MCP Server with 5 tools
- [x] OpenAI Agents configuration
- [x] Natural language parsing
- [x] Integration with Phase 2 backend
- [x] Responsive chat interface
- [x] Loading states
- [x] Error handling
- [x] MCP tool contracts documented

## Security

- **Domain Allowlist**: OpenAI domain only (`openai.com`)
- **User Isolation**: All operations scoped to `user_id`
- **API Key Security**: Store in environment variables
- **JWT Tokens**: Phase 2 authentication reused

## Known Limitations

1. **Natural Language Processing**: Currently uses regex-based pattern matching. Full OpenAI Agents SDK integration will provide more sophisticated NLP capabilities.

2. **Multi-turn Conversations**: Context is not maintained across messages. Each message is processed independently.

3. **MCP Server Communication**: For demo purposes, the chat UI calls the FastAPI backend directly. Full MCP protocol implementation requires client-side MCP SDK.

## Future Enhancements

- Full OpenAI Agents SDK integration with tool calling
- Multi-turn conversations with context memory
- Task suggestions based on patterns
- Smart task prioritization
- Reminder scheduling integration
- Voice input support

## Documentation

- [Specification](specs/spec.md)
- [MCP Tools Contract](specs/contracts/mcp-tools.md)
- [Claude Code Rules](CLAUDE.md)
- [Constitution](.specify/memory/constitution.md)

---

**Phase**: 3 of 5
**Status**: Complete ✅
**Last Updated**: 2025-12-30
