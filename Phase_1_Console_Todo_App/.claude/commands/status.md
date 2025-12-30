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
README.md → First 10 lines → Extract phase name
CLAUDE.md → "Technology Stack" section → Extract language, framework, storage
Git branch → Current branch name
```

### 2. Progress Calculation (10 seconds max)

Scan checklist file:

```
specs/checklists/requirements.md → Count [x] vs [ ] patterns
Formula: completion = (checked / total) * 100
```

If no checklist exists, scan `specs/spec.md` for:
- Functional Requirements section → Count FR-XXX items
- Cross-reference with `specs/tasks.md` completed items

### 3. Milestone Summary (5 seconds max)

List files only (no content read):

```
history/prompts/*.prompt.md → Last 3 filenames by sort order
history/adr/*.md → Last 3 filenames by sort order
Extract slugs from filenames only
```

### 4. Next Tasks (5 seconds max)

Scan `specs/tasks.md`:

```
Find first "[ ]" items (up to 3)
Extract task descriptions only
```

### 5. Risk Detection (5 seconds max)

Check file existence:

```
specs/spec.md → exists?
specs/plan.md → exists?
specs/tasks.md → exists?
specs/checklists/ → has files?
history/prompts/ → has files?
```

Flag any missing as risk.

## Output Format

Use this EXACT template:

```markdown
## Project Status Report

### Phase Identity
**Phase**: [Phase Name from README]
**Tech Stack**: [Language] | [Framework] | [Storage Type]
**Branch**: [Current Git Branch]

### Current Progress
**Completion**: [XX]% ([completed]/[total] items)
**Status**: [On Track | At Risk | Blocked]

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

**Critical files**: spec.md, plan.md, tasks.md
**Non-critical files**: checklists/, history/

## Performance Targets

| Metric | Target |
|--------|--------|
| Execution Time | < 30 seconds |
| Files Scanned | < 10 |
| Lines Read | < 200 total |
| Output Tokens | < 300 |

## Error Handling

| Scenario | Action |
|----------|--------|
| README.md missing | Use folder name as phase |
| CLAUDE.md missing | Report "Tech stack not documented" |
| specs/ empty | Report "Specification phase not started" |
| history/ empty | Report "No history recorded yet" |

## DO NOT

- Read source code files (*.py, *.ts, *.js, etc.)
- Analyze implementation details
- Provide recommendations or suggestions
- Ask follow-up questions
- Create PHR for this command (too lightweight)

## Example Output

```markdown
## Project Status Report

### Phase Identity
**Phase**: Phase 1 - Console Todo App
**Tech Stack**: Python 3.13 | UV | In-Memory
**Branch**: 001-console-todo

### Current Progress
**Completion**: 100% (14/14 items)
**Status**: On Track

### Completed Milestones (Last 3)
1. 003-generate-task-breakdown.tasks
2. 002-complete-implementation-plan.plan
3. 001-create-phase1-spec.spec

### Next Immediate Tasks
- [ ] All tasks completed

### Blocked/Risks
None detected

---
*Generated: 2025-12-29 14:30 | Mode: Fast Scan*
```
