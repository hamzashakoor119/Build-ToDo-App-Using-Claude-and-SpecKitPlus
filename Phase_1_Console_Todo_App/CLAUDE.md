# Phase 1: Console Todo App - Claude Code Rules

## Project Context

**Phase**: 1 of 5 - In-Memory Python Console App
**Scope**: Basic Todo CRUD operations via command-line interface
**Status**: Self-contained, portable project folder

## Technology Stack (Phase 1 Specific)

- **Language**: Python 3.13+
- **Package Manager**: UV
- **Architecture**: In-memory storage (no database)
- **Interface**: Interactive CLI + Command-line arguments
- **Testing**: pytest with coverage

## Project Structure

```
Phase_1_Console_Todo_App/
├── .claude/              # Claude Code configuration
│   ├── commands/         # Slash commands (/sp.specify, /sp.plan, etc.)
│   └── skills/           # Domain-specific skills
├── .specify/             # SpecKit Plus configuration
│   ├── memory/           # Constitution and session state
│   └── templates/        # Spec, plan, task templates
├── specs/                # Feature specifications
│   ├── checklists/       # Requirements checklists
│   ├── contracts/        # CLI interface contracts
│   ├── spec.md           # Main specification
│   ├── plan.md           # Implementation plan
│   └── tasks.md          # Task breakdown
├── history/              # Development history
│   ├── prompts/          # Prompt History Records (PHRs)
│   └── adr/              # Architecture Decision Records
├── src/                  # Source code
│   └── todo_app/         # Main application package
├── tests/                # Test suite
├── main.py               # Entry point
├── pyproject.toml        # Python project config
└── README.md             # Phase documentation
```

## Core Features (Basic Level)

1. **Add Task**: Create new todo items with title and optional description
2. **Delete Task**: Remove tasks by ID
3. **Update Task**: Modify task title or description
4. **View Tasks**: List all tasks with status
5. **Mark Complete**: Toggle task completion status

## Development Guidelines

### Spec-Driven Development
- All code must be generated from specifications
- Specs live in `/specs` directory
- Use `/sp.specify`, `/sp.plan`, `/sp.tasks` commands

### PHR Requirements
After completing tasks, create PHR in `history/prompts/`:
- Stage: spec | plan | tasks | red | green | refactor
- Route: `history/prompts/<ID>-<slug>.<stage>.prompt.md`

### Test-First Development
- Write tests before implementation
- All tests must pass before completion
- Use pytest for testing

### Code Quality
- Clean, readable Python code
- Type hints where beneficial
- Docstrings for public functions
- No hardcoded values - use configuration

## Quick Commands

### `/status` or `/summary` - Instant Project Report
Get an instant, fact-based project status report with minimal latency.

**What it does**:
- Scans specs/, history/, and metadata files (NOT source code)
- Calculates progress from checklists
- Lists recent milestones (last 3 PHRs/ADRs)
- Shows next pending tasks
- Detects missing files as risks

**Output includes**:
- Phase Identity & Tech Stack
- Completion percentage
- Completed milestones
- Next immediate tasks
- Blocked/Risks

**Performance**: < 30 seconds, < 300 output tokens

**Skill location**: `.claude/skills/project-intelligence/SKILL.md`

## CLI Interface Contract

```bash
# Interactive mode
python main.py

# Command-line mode
python -m todo_app add "Task title"
python -m todo_app list
python -m todo_app complete <id>
python -m todo_app delete <id>
python -m todo_app update <id> "New title"
```

## Success Criteria

- [ ] All 5 basic features implemented
- [ ] Interactive CLI working
- [ ] All tests passing
- [ ] Clean project structure
- [ ] Documentation complete

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

### Skill Naming Convention
```
<action>-<target>-<context>
Examples:
- api-endpoint-generator
- docker-build-fixer
- test-coverage-checker
- db-migration-handler
- component-scaffold-react
```

### Minimum Skill Content
```markdown
# <Skill Name>

## Auto-Generated
- **Trigger**: What caused this skill to be created
- **Created**: <date>
- **Reuse Count**: 0

## Purpose
<One line description>

## When to Use
<Trigger conditions>

## Steps
1. <Step 1>
2. <Step 2>
...

## Code/Templates
<Reusable code blocks>

## Errors & Solutions
<Known issues and fixes>
```

### Examples of Auto-Skill Detection

**Example 1: Repetition Detected**
```
User asks: "Create a new API endpoint for users"
Claude creates endpoint...

User asks: "Create a new API endpoint for products"
Claude detects: Same pattern as before!
Claude: "🔧 Auto-Skill Detected: API Endpoint Generator"
Creates: .claude/skills/api-endpoint-generator/SKILL.md
Then uses skill to create products endpoint faster
```

**Example 2: Error Pattern Detected**
```
User: "Fix this import error"
Claude fixes...

User: "Another import error here"
Claude detects: Same error type!
Claude: "🔧 Auto-Skill Detected: Import Error Handler"
Creates: .claude/skills/import-error-handler/SKILL.md
Includes: Common causes, solutions, prevention tips
```

**Example 3: Complex Workflow Detected**
```
User: "Set up database with migrations"
Claude does 8 steps...

Claude detects: This was complex and reusable!
Claude: "🔧 Auto-Skill Detected: Database Setup Workflow"
Creates: .claude/skills/db-setup-workflow/SKILL.md
Next time: Single command instead of 8 steps
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

### Skill Evolution

Skills should improve over time:
```
- Add new edge cases when discovered
- Add better error handling
- Add more code templates
- Update based on new patterns
- Mark deprecated sections
```

### CRITICAL RULES

1. **NEVER** repeat complex work without creating a skill
2. **ALWAYS** check existing skills before starting
3. **IMMEDIATELY** create skill when trigger detected
4. **ANNOUNCE** skill creation to user
5. **USE** skill-factory as reference for skill structure
6. **SAVE** all skills in .claude/skills/<name>/SKILL.md
