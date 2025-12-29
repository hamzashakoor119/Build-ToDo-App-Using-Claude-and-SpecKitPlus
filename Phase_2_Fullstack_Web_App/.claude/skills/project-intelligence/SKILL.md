# Project Intelligence - Instant Status & Summary Skill

## Auto-Generated
- **Trigger**: Requested for instant project status without latency
- **Created**: 2025-12-29
- **Adapted From**: Phase 1 Console Todo App
- **Reuse Count**: 0

## Purpose
Provide instantaneous project summaries and status reports with minimal token consumption and zero "thinking" delays.

## Trigger Conditions
- User types `/status` or `/summary`
- User asks "What's the project status?"
- User asks "Give me a summary"
- User asks "Where are we?"

## Design Principles

### Token Optimization Strategy
1. **Metadata-First**: Scan folder structures and file headers, not full content
2. **Checklist Parsing**: Extract only `[x]` and `[ ]` patterns from checklists
3. **Fixed Template**: Use standardized output format to avoid generation overhead
4. **No Code Reading**: Never read source code files for status
5. **Cache-Friendly**: Same inputs always produce same structure

## Inputs Required
None - automatically scans the following locations:
- `specs/spec.md` - Feature specification (header only)
- `specs/checklists/requirements.md` - Progress tracking
- `specs/tasks.md` - Task breakdown
- `history/prompts/` - PHR files (count + last 3)
- `history/adr/` - ADR files (count + last 3)
- `README.md` - Phase identity
- `CLAUDE.md` - Tech stack

## Phase 2 Specific Scans
- `frontend/package.json` - Frontend dependencies version check
- `backend/requirements.txt` - Backend dependencies check
- `frontend/src/app/` - App Router pages count
- `backend/app/routers/` - API endpoints count

## Execution Steps

### Step 1: Phase Identity Extraction (5 seconds max)
```
SCAN: README.md first 20 lines
EXTRACT: Phase name, description
SCAN: CLAUDE.md "Technology Stack" section
EXTRACT: Frontend (Next.js), Backend (FastAPI), Database (Neon PostgreSQL)
```

### Step 2: Progress Calculation (10 seconds max)
```
READ: specs/tasks.md
COUNT: Lines matching "[x]" = completed
COUNT: Lines matching "[ ]" = pending
CALCULATE: % = completed / (completed + pending) * 100
```

### Step 3: Milestone Summary (5 seconds max)
```
LIST: history/prompts/*.prompt.md (last 3 by name)
LIST: history/adr/*.md (last 3 by name)
EXTRACT: Filename slugs only (no content read)
```

### Step 4: Next Tasks Extraction (5 seconds max)
```
READ: specs/tasks.md
FIND: First section with "[ ]" items
EXTRACT: Up to 3 pending items
```

### Step 5: Risk Detection (5 seconds max)
```
CHECK: specs/spec.md exists?
CHECK: specs/plan.md exists?
CHECK: specs/tasks.md exists?
CHECK: frontend/src/app/page.tsx exists?
CHECK: backend/app/main.py exists?
CHECK: history/prompts/ has files?
FLAG: Any missing = risk
```

## Output Format (Fixed Template)

```markdown
## Project Status Report

### Phase Identity
**Phase**: [Phase Name]
**Tech Stack**: Next.js + FastAPI | TypeScript/Python | Neon PostgreSQL
**Branch**: [Current Git Branch]

### Current Progress
**Completion**: [XX]% ([completed]/[total] tasks)
**Status**: [On Track | At Risk | Blocked]

### Component Status
| Component | Status | Files |
|-----------|--------|-------|
| Frontend | [Ready/In Progress/Not Started] | [count] |
| Backend | [Ready/In Progress/Not Started] | [count] |
| Database | [Connected/Pending] | - |

### Completed Milestones (Last 3)
1. [PHR/ADR slug 1]
2. [PHR/ADR slug 2]
3. [PHR/ADR slug 3]

### Next Immediate Tasks
- [ ] [Task 1 from tasks.md]
- [ ] [Task 2 from tasks.md]
- [ ] [Task 3 from tasks.md]

### Blocked/Risks
[List missing files or "None detected"]

---
*Generated: [timestamp] | Tokens: ~minimal*
```

## Error Handling

| Error | Response |
|-------|----------|
| specs/spec.md missing | Report "Specification not found - run /sp.specify" |
| specs/tasks.md missing | Report "Tasks not generated - run /sp.tasks" |
| history/prompts/ empty | Report "No PHRs recorded yet" |
| frontend/ missing | Report "Frontend not initialized - run npm create next-app" |
| backend/ missing | Report "Backend not initialized" |

## Quick Execution Script

For Claude to execute this skill:

```
1. DO NOT read source code files (*.py, *.ts, *.tsx, etc.)
2. DO NOT analyze implementation details
3. ONLY scan metadata files: md, toml, json headers
4. USE glob patterns for file counting
5. EXTRACT first 5 lines for identification
6. PARSE checklists with regex: /\[(x| )\]/g
7. OUTPUT using fixed template above
8. TOTAL TIME: Under 30 seconds
```

## Examples

### Example 1: Phase 2 In Progress
```markdown
## Project Status Report

### Phase Identity
**Phase**: Phase 2 - Full-Stack Web Todo App
**Tech Stack**: Next.js + FastAPI | TypeScript/Python | Neon PostgreSQL
**Branch**: 002-fullstack-web-app

### Current Progress
**Completion**: 62% (50/80 tasks)
**Status**: On Track

### Component Status
| Component | Status | Files |
|-----------|--------|-------|
| Frontend | In Progress | 15 |
| Backend | Ready | 12 |
| Database | Connected | - |

### Completed Milestones (Last 3)
1. T050-add-task-validation
2. T043-api-task-list
3. T034-auth-logout

### Next Immediate Tasks
- [ ] T051 Add toggle_complete function to task_service.py
- [ ] T052 Implement PATCH /api/{user_id}/tasks/{task_id}/complete
- [ ] T053 Add checkbox to TaskItem.tsx

### Blocked/Risks
None detected

---
*Generated: 2025-12-29 | Tokens: ~minimal*
```

## Integration

### Slash Command: /status
Located at: `.claude/commands/status.md`

### Alternative Trigger: /summary
Same output, different trigger phrase.

## Performance Targets

| Metric | Target |
|--------|--------|
| Execution Time | < 30 seconds |
| Token Usage | < 500 tokens output |
| Files Read | < 15 files |
| Lines Scanned | < 300 lines total |
| Accuracy | 100% fact-based |

---

## Version
- **Version**: 1.0.0
- **Created**: 2025-12-29
- **Category**: Project Intelligence
- **Reuse Potential**: High (adapted for fullstack phases)
