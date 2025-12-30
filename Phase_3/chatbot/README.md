# Todo Chatbot UI

AI-powered chatbot interface for managing tasks through natural language.

## Features

- Natural language task management
- Real-time conversation with AI
- Uses OpenAI Agents SDK
- Connects to MCP Server for task operations

## Setup

1. Install dependencies:
```bash
npm install
```

2. Create `.env.local`:
```
OPENAI_API_KEY=your_openai_api_key
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
NEXT_PUBLIC_MCP_SERVER_URL=http://localhost:3001
BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your_secret_key_min_32_chars
```

3. Run development server:
```bash
npm run dev
```

4. Open http://localhost:3000

## Natural Language Commands

- "Add a task to buy groceries"
- "Show me all my tasks"
- "Mark task #1 as done"
- "Delete task #3"
- "Update task #1 title to 'Buy organic groceries'"

## Architecture

```
User Input → Chat UI → OpenAI Agents → MCP Server → FastAPI Backend → Database
```
