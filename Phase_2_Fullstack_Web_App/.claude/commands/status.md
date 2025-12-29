---
description: Instant project status report with minimal latency and token usage.
---

## User Input

```text
$ARGUMENTS
```

You **MAY** consider the user input for filtering (if not empty).

## Goal

Provide an instantaneous, fact-based project status report by scanning metadata files only. This command prioritizes speed and token efficiency over comprehensive analysis.

## Operating Constraints

**SPEED-FIRST**: Complete within 30 seconds. No deep file reads.
**METADATA-ONLY**: Scan checklists, headers, and file counts. Never read source code.
**FIXED TEMPLATE**: Use the exact output format below. No variations.
**ZERO HALLUCINATION**: Report only what exists in files. Mark missing items clearly.

## Execution Steps

### 1. Phase Identity (5 seconds max)

Scan these files for identity information:

```
README.md -> First 10 lines -> Extract phase name
CLAUDE.md -> "Technology Stack" section -> Extract frontend, backend, database
Git branch -> Current branch name
```

### 2. Progress Calculation (10 seconds max)

Scan tasks file:

```
specs/tasks.md -> Count [x] vs [ ] patterns
Formula: completion = (checked / total) * 100
```

### 3. Component Status (5 seconds max)

Quick file counts:

```
frontend/src/app/ -> Count *.tsx files
frontend/src/components/ -> Count *.tsx files
backend/app/routers/ -> Count *.py files
backend/app/services/ -> Count *.py files
```

### 4. Milestone Summary (5 seconds max)

List files only (no content read):

```
history/prompts/*.prompt.md -> Last 3 filenames by sort order
history/adr/*.md -> Last 3 filenames by sort order
Extract slugs from filenames only
```

### 5. Next Tasks (5 seconds max)

Scan `specs/tasks.md`:

```
Find first "[ ]" items (up to 3)
Extract task descriptions only
```

### 6. Risk Detection (5 seconds max)

Check file existence:

```
specs/spec.md -> exists?
specs/plan.md -> exists?
specs/tasks.md -> exists?
frontend/src/app/page.tsx -> exists?
backend/app/main.py -> exists?
frontend/.env.local -> exists? (warn if missing)
backend/.env -> exists? (warn if missing)
```

Flag any missing as risk.

## Output Format

Use this EXACT template:

```markdown
## Project Status Report

### Phase Identity
**Phase**: [Phase Name from README]
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
| Auth | [Configured/Pending] | - |
| Database | [Connected/Pending] | - |

### Completed Milestones (Last 3)
1. [PHR/ADR slug or "None recorded"]
2. [PHR/ADR slug or "-"]
3. [PHR/ADR slug or "-"]

### Next Immediate Tasks
- [ ] [Task 1 or "All tasks completed"]
- [ ] [Task 2 or "-"]
- [ ] [Task 3 or "-"]

### Blocked/Risks
[List missing files or "None detected"]

---
*Generated: [YYYY-MM-DD HH:MM] | Mode: Fast Scan*
```

## Status Determination Rules

| Condition | Status |
|-----------|--------|
| All core files exist + >75% complete | On Track |
| Missing 1-2 non-critical files OR 50-75% complete | At Risk |
| Missing critical files OR <50% complete OR blockers | Blocked |

**Critical files**: spec.md, plan.md, tasks.md, frontend/src/app/page.tsx, backend/app/main.py
**Non-critical files**: checklists/, history/, .env files

## Component Status Rules

| Component | Ready When | In Progress When | Not Started When |
|-----------|------------|------------------|------------------|
| Frontend | >10 tsx files | 1-10 tsx files | 0 tsx files |
| Backend | >5 py files in routers/ | 1-5 py files | 0 py files |
| Auth | auth.ts exists + middleware | partial files | nothing |
| Database | database.py + .env has DB_URL | database.py only | no files |

## Performance Targets

| Metric | Target |
|--------|--------|
| Execution Time | < 30 seconds |
| Files Scanned | < 15 |
| Lines Read | < 300 total |
| Output Tokens | < 400 |

## Error Handling

| Scenario | Action |
|----------|--------|
| README.md missing | Use folder name as phase |
| CLAUDE.md missing | Report "Tech stack not documented" |
| specs/ empty | Report "Specification phase not started" |
| history/ empty | Report "No history recorded yet" |
| frontend/ missing | Report "Frontend not initialized" |
| backend/ missing | Report "Backend not initialized" |

## DO NOT

- Read source code files (*.py, *.ts, *.tsx, etc.)
- Analyze implementation details
- Provide recommendations or suggestions
- Ask follow-up questions
- Create PHR for this command (too lightweight)

## Example Output

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
| Frontend | In Progress | 12 |
| Backend | Ready | 8 |
| Auth | Configured | - |
| Database | Connected | - |

### Completed Milestones (Last 3)
1. T050-add-task-validation
2. T043-api-task-list
3. T034-auth-logout

### Next Immediate Tasks
- [ ] T051 Add toggle_complete to task_service.py
- [ ] T052 Implement PATCH endpoint
- [ ] T053 Add checkbox to TaskItem.tsx

### Blocked/Risks
- frontend/.env.local missing - copy from .env.example

---
*Generated: 2025-12-29 15:00 | Mode: Fast Scan*
```
