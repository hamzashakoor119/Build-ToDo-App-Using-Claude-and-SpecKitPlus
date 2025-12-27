# Session Management System

## Overview
This directory stores session states for pause/resume functionality.

## Usage

### Save Session (Stop Work)
When you want to stop work:
```
You: stop <session-id>
Claude: (Saves current state to session-<id>-state.md)
```

### Resume Session (Continue Work)
When you want to resume:
```
You: resume <session-id>
Claude: (Reads session-<id>-state.md and provides full context)
```

## Session File Format

Each session has:
- `session-<id>-state.md` - Human-readable summary
- `session-<id>-context.json` - Machine-readable data (optional)

## Session State Content

1. **Last Activity** - When and what
2. **Progress Summary** - Completed, In Progress, Pending
3. **Active Todos** - Current task list
4. **Current Context** - What file, what command, next step
5. **Important Decisions** - ADRs, tech choices
6. **Files Modified** - Track changes
7. **Environment** - Tech stack, dependencies
8. **Notes** - Important reminders

## Example

```markdown
# Session 317 - Evolution of Todo

## Last Activity
- **Date**: 2025-12-26 15:30
- **Phase**: Phase I
- **Feature**: Task model

## Progress Summary
### Completed:
- ✅ Constitution created
- ✅ Specs written

### In Progress:
- 🔄 Task model implementation

### Pending:
- ⏳ CLI interface
- ⏳ Tests

## Current Context
Working on: src/models/task.py
Next step: Complete validation logic

## Notes
- Spec-driven approach mandatory
- Test-first development
```

## Benefits

✅ **Resume exactly where you left off**
✅ **Context never lost**
✅ **Progress tracking**
✅ **Multiple sessions support**
✅ **Cross-terminal compatibility**

## Commands Quick Reference

| Command | Purpose |
|---------|---------|
| `stop <id>` | Save current session |
| `resume <id>` | Load session and continue |
| `list sessions` | Show all saved sessions |
| `delete <id>` | Remove old session |
