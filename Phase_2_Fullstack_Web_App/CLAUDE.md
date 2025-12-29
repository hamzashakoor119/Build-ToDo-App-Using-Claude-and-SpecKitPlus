# Phase 2: Fullstack Web App - Claude Code Rules

## Project Context

**Phase**: 2 of 5 - Full-Stack Web Application
**Scope**: Web-based Todo app with authentication and persistent storage
**Status**: Self-contained, portable project folder

## Technology Stack (Phase 2 Specific)

### Frontend
- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Auth Client**: Better Auth

### Backend
- **Framework**: FastAPI (Python)
- **ORM**: SQLModel
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT

## Project Structure

```
Phase_2_Fullstack_Web_App/
├── .claude/              # Claude Code configuration
│   ├── commands/         # Slash commands
│   └── skills/           # Domain-specific skills
├── .specify/             # SpecKit Plus configuration
│   ├── memory/           # Constitution and session state
│   └── templates/        # Spec, plan, task templates
├── specs/                # Feature specifications
│   ├── checklists/       # Requirements checklists
│   ├── contracts/        # API contracts (OpenAPI)
│   ├── spec.md           # Main specification
│   ├── plan.md           # Implementation plan
│   └── tasks.md          # Task breakdown
├── history/              # Development history
│   ├── prompts/          # Prompt History Records (PHRs)
│   └── adr/              # Architecture Decision Records
├── frontend/             # Next.js application
│   ├── src/
│   │   ├── app/          # App Router pages
│   │   ├── components/   # React components
│   │   └── types/        # TypeScript types
│   └── CLAUDE.md         # Frontend-specific guidance
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── models/       # SQLModel models
│   │   ├── routers/      # API endpoints
│   │   ├── schemas/      # Pydantic schemas
│   │   └── services/     # Business logic
│   └── CLAUDE.md         # Backend-specific guidance
└── README.md             # Phase documentation
```

## Core Features (Basic Level + Auth)

1. **Add Task**: Create new todo items
2. **Delete Task**: Remove tasks by ID
3. **Update Task**: Modify task details
4. **View Tasks**: List all user's tasks
5. **Mark Complete**: Toggle task completion
6. **User Authentication**: Register, Login, Logout
7. **User Sessions**: JWT-based session management

## Development Guidelines

### Spec-Driven Development
- All code must be generated from specifications
- Specs live in `/specs` directory
- Use `/sp.specify`, `/sp.plan`, `/sp.tasks` commands

### PHR Requirements
After completing tasks, create PHR in `history/prompts/`:
- Stage: spec | plan | tasks | red | green | refactor
- Route: `history/prompts/<ID>-<slug>.<stage>.prompt.md`

### API Standards
- RESTful conventions
- JSON request/response
- Consistent error responses
- Input validation
- JWT authentication required for protected routes

### Database Standards
- SQLModel for all operations
- Proper relationships
- Environment-based connection strings
- No raw SQL queries

## API Contract Overview

```yaml
# Authentication
POST   /api/auth/register    # Create new user
POST   /api/auth/login       # User login
POST   /api/auth/logout      # User logout

# Tasks (Protected)
GET    /api/tasks            # List user's tasks
POST   /api/tasks            # Create task
GET    /api/tasks/{id}       # Get single task
PUT    /api/tasks/{id}       # Update task
DELETE /api/tasks/{id}       # Delete task
PATCH  /api/tasks/{id}/complete  # Toggle completion
```

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret-key
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Success Criteria

- [ ] Responsive web UI with all Basic Level features
- [ ] RESTful API with proper endpoints
- [ ] Better Auth authentication working
- [ ] JWT token verification
- [ ] Neon DB integrated
- [ ] All tests passing
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
