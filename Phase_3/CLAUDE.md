# Phase 3: AI-Powered Todo Chatbot - Claude Code Rules

## Project Context

**Phase**: 3 of 5 - AI-Powered Todo Chatbot
**Scope**: Natural language task management via AI chatbot
**Status**: Self-contained, portable project folder

## Technology Stack (Phase 3 Specific)

- **Frontend UI**: OpenAI ChatKit
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK (Python)
- **Backend**: FastAPI (from Phase 2)
- **Database**: Neon PostgreSQL (from Phase 2)
- **Architecture**: Stateless chat endpoint with database-persisted conversation state

## Project Structure

```
Phase_3/
├── .claude/              # Claude Code configuration
│   ├── commands/         # Slash commands
│   └── skills/           # Domain-specific skills
├── .specify/             # SpecKit Plus configuration
│   ├── memory/           # Constitution and session state
│   └── templates/        # Spec, plan, task templates
├── specs/                # Feature specifications
│   ├── checklists/       # Requirements checklists
│   ├── contracts/        # MCP tool contracts
│   ├── spec.md           # Main specification
│   ├── plan.md           # Implementation plan
│   └── tasks.md          # Task breakdown
├── history/              # Development history
│   ├── prompts/          # Prompt History Records (PHRs)
│   └── adr/              # Architecture Decision Records
├── chatbot/              # ChatKit UI
├── mcp-server/           # MCP Server implementation
│   └── tools/            # MCP tools
├── agents/               # OpenAI Agents configuration
└── README.md             # Phase documentation
```

## Core Features

All Basic Level features via natural language:
1. **Add Task**: "Add a task to buy groceries"
2. **Delete Task**: "Delete task #3"
3. **Update Task**: "Update task #1 title to 'Buy organic groceries'"
4. **View Tasks**: "Show me all my tasks"
5. **Mark Complete**: "Mark task #2 as done"

## MCP Tools Contract

```yaml
# Required MCP Tools
add_task:
  description: Create a new task
  parameters:
    - title: string (required)
    - description: string (optional)
  returns: task object

list_tasks:
  description: List all user's tasks
  parameters:
    - filter: string (optional: all, completed, pending)
  returns: array of task objects

complete_task:
  description: Mark task as complete/incomplete
  parameters:
    - id: integer (required)
  returns: updated task object

delete_task:
  description: Delete a task
  parameters:
    - id: integer (required)
  returns: success boolean

update_task:
  description: Update task details
  parameters:
    - id: integer (required)
    - title: string (optional)
    - description: string (optional)
  returns: updated task object
```

## Development Guidelines

### Spec-Driven Development
- All code must be generated from specifications
- MCP tools must have contracts defined
- Use `/sp.specify`, `/sp.plan`, `/sp.tasks` commands

### MCP Tool Standards
- Stateless tools that store state in database
- Clear parameter definitions
- Consistent return format
- Error handling with meaningful messages
- Tool naming: verb_noun format

### PHR Requirements
After completing tasks, create PHR in `history/prompts/`:
- Stage: spec | plan | tasks | red | green | refactor
- Route: `history/prompts/<ID>-<slug>.<stage>.prompt.md`

## Success Criteria

- [ ] ChatKit UI integrated
- [ ] OpenAI Agents SDK functional
- [ ] MCP server with all 5 tools
- [ ] Stateless architecture with DB-persisted conversations
- [ ] Natural language task management working
- [ ] OpenAI domain allowlist configured

## Phase Independence

This folder is designed to be **self-contained**. It can be:
- Moved out of the parent project
- Opened independently in Claude Code
- Developed without context pollution from other phases

All specs, history, and configuration are local to this phase.

---

## AUTO-SKILL SYSTEM (MANDATORY)

### Purpose
Claude MUST automatically create reusable skills when detecting patterns that save time or reduce repetition. This is NOT optional - it's a core behavior.

### Auto-Skill Triggers (MUST Create Skill When):

| Trigger | Detection Pattern | Action |
|---------|------------------|--------|
| **Repetition** | Same task done 2+ times | Create skill immediately |
| **Time-Consuming** | Task takes 5+ steps | Create skill for automation |
| **Error-Prone** | Same error fixed 2+ times | Create error-handler skill |
| **Boilerplate** | Similar code generated 2+ times | Create generator skill |
| **Complex Workflow** | Multi-step process | Create workflow skill |
| **External Integration** | API/Service setup | Create integration skill |

### Auto-Skill Creation Process

When trigger detected, Claude MUST:

```
1. STOP current task briefly
2. ANNOUNCE: "🔧 Auto-Skill Detected: [pattern name]"
3. CREATE skill at: .claude/skills/<skill-name>/SKILL.md
4. INCLUDE in skill:
   - What triggered this skill
   - Step-by-step instructions
   - Code templates (if applicable)
   - Error handling
   - Usage examples
5. RESUME original task using the new skill
6. LOG: "✅ Skill created: <skill-name> - Future uses will be faster"
```

### Skill Reuse Protocol

Before starting ANY task, Claude MUST:
```
1. CHECK .claude/skills/ for existing relevant skills
2. IF skill exists:
   - USE the skill
   - UPDATE skill if improvements found
   - INCREMENT reuse count
3. IF no skill exists:
   - Proceed with task
   - WATCH for skill triggers
   - CREATE skill if triggered
```

### CRITICAL RULES

1. **NEVER** repeat complex work without creating a skill
2. **ALWAYS** check existing skills before starting
3. **IMMEDIATELY** create skill when trigger detected
4. **ANNOUNCE** skill creation to user
5. **USE** skill-factory as reference for skill structure
6. **SAVE** all skills in .claude/skills/<name>/SKILL.md
