# Skill Factory - Master Skill Generator

## Purpose
This is the **META-SKILL** that teaches Claude how to create new skills on demand. When you need a new capability, Claude will reference this skill to generate a fully functional, production-ready skill.

## Trigger Phrases
- "Create a skill for..."
- "I need a new skill that..."
- "Generate a skill to handle..."
- "Build me a skill for..."

---

## Skill Architecture Blueprint

### Standard Skill Structure
```
.claude/skills/<skill-name>/
├── SKILL.md           # Main skill definition (required)
├── templates/         # Code/config templates (optional)
├── scripts/           # Executable scripts (optional)
├── examples/          # Usage examples (optional)
└── tests/             # Skill tests (optional)
```

### SKILL.md Template
```markdown
# <Skill Name>

## Purpose
<One-line description of what this skill does>

## Trigger Conditions
<When should Claude activate this skill>

## Inputs Required
<What information Claude needs to execute>

## Execution Steps
<Step-by-step instructions>

## Output Format
<What the skill produces>

## Code Templates
<Reusable code blocks>

## Error Handling
<How to handle failures>

## Examples
<Real usage examples>
```

---

## Skill Categories & Patterns

### Category 1: Code Generator Skills
**Purpose:** Generate boilerplate code, components, or modules

```markdown
# Example: Component Generator Skill

## Purpose
Generate React/Next.js components with proper structure

## Inputs Required
- Component name
- Component type (page, component, layout)
- Props interface
- Features needed (state, effects, API calls)

## Execution Steps
1. Analyze component requirements
2. Select appropriate template
3. Generate TypeScript interface for props
4. Generate component code
5. Generate test file
6. Generate story file (if Storybook)

## Code Templates

### Functional Component Template
\`\`\`tsx
import React from 'react';

interface {{ComponentName}}Props {
  {{props}}
}

export const {{ComponentName}}: React.FC<{{ComponentName}}Props> = ({
  {{destructuredProps}}
}) => {
  return (
    <div className="{{className}}">
      {{content}}
    </div>
  );
};

export default {{ComponentName}};
\`\`\`

### Component with State Template
\`\`\`tsx
import React, { useState, useEffect } from 'react';

interface {{ComponentName}}Props {
  {{props}}
}

export const {{ComponentName}}: React.FC<{{ComponentName}}Props> = ({
  {{destructuredProps}}
}) => {
  const [{{stateName}}, set{{StateName}}] = useState<{{stateType}}>({{initialValue}});

  useEffect(() => {
    {{effectLogic}}
  }, [{{dependencies}}]);

  return (
    <div className="{{className}}">
      {{content}}
    </div>
  );
};
\`\`\`
```

### Category 2: API/Backend Skills
**Purpose:** Generate API endpoints, database operations, middleware

```markdown
# Example: API Endpoint Generator Skill

## Purpose
Generate FastAPI endpoints with proper validation and error handling

## Inputs Required
- Resource name (e.g., "tasks", "users")
- Operations needed (CRUD or specific)
- Authentication required?
- Request/Response schemas

## Code Templates

### FastAPI Router Template
\`\`\`python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.database import get_session
from app.models.{{resource}} import {{Resource}}
from app.schemas.{{resource}} import {{Resource}}Create, {{Resource}}Update, {{Resource}}Response

router = APIRouter(prefix="/{{resources}}", tags=["{{resources}}"])

@router.get("/", response_model=List[{{Resource}}Response])
async def list_{{resources}}(
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
):
    """List all {{resources}}"""
    statement = select({{Resource}}).offset(skip).limit(limit)
    results = session.exec(statement).all()
    return results

@router.post("/", response_model={{Resource}}Response, status_code=status.HTTP_201_CREATED)
async def create_{{resource}}(
    {{resource}}: {{Resource}}Create,
    session: Session = Depends(get_session)
):
    """Create a new {{resource}}"""
    db_{{resource}} = {{Resource}}.model_validate({{resource}})
    session.add(db_{{resource}})
    session.commit()
    session.refresh(db_{{resource}})
    return db_{{resource}}

@router.get("/{{{resource}}_id}", response_model={{Resource}}Response)
async def get_{{resource}}(
    {{resource}}_id: int,
    session: Session = Depends(get_session)
):
    """Get a specific {{resource}}"""
    {{resource}} = session.get({{Resource}}, {{resource}}_id)
    if not {{resource}}:
        raise HTTPException(status_code=404, detail="{{Resource}} not found")
    return {{resource}}

@router.put("/{{{resource}}_id}", response_model={{Resource}}Response)
async def update_{{resource}}(
    {{resource}}_id: int,
    {{resource}}_update: {{Resource}}Update,
    session: Session = Depends(get_session)
):
    """Update a {{resource}}"""
    {{resource}} = session.get({{Resource}}, {{resource}}_id)
    if not {{resource}}:
        raise HTTPException(status_code=404, detail="{{Resource}} not found")

    update_data = {{resource}}_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr({{resource}}, key, value)

    session.add({{resource}})
    session.commit()
    session.refresh({{resource}})
    return {{resource}}

@router.delete("/{{{resource}}_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_{{resource}}(
    {{resource}}_id: int,
    session: Session = Depends(get_session)
):
    """Delete a {{resource}}"""
    {{resource}} = session.get({{Resource}}, {{resource}}_id)
    if not {{resource}}:
        raise HTTPException(status_code=404, detail="{{Resource}} not found")
    session.delete({{resource}})
    session.commit()
\`\`\`
```

### Category 3: DevOps/Infrastructure Skills
**Purpose:** Generate Docker, K8s, CI/CD configurations

```markdown
# Example: Dockerfile Generator Skill

## Purpose
Generate optimized Dockerfiles for different application types

## Inputs Required
- Application type (python, node, go, etc.)
- Base image preference
- Build requirements
- Runtime requirements
- Port to expose

## Code Templates

### Python FastAPI Dockerfile
\`\`\`dockerfile
# Build stage
FROM python:3.13-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Production stage
FROM python:3.13-slim

WORKDIR /app

# Create non-root user
RUN addgroup --system app && adduser --system --group app

# Install runtime dependencies
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*

# Copy application
COPY --chown=app:app . .

# Switch to non-root user
USER app

# Expose port
EXPOSE {{port}}

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:{{port}}/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "{{port}}"]
\`\`\`

### Next.js Dockerfile
\`\`\`dockerfile
# Dependencies stage
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

# Builder stage
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

# Production stage
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE {{port}}

CMD ["node", "server.js"]
\`\`\`
```

### Category 4: Error Handler Skills
**Purpose:** Handle specific error types with recovery strategies

```markdown
# Example: Database Error Handler Skill

## Trigger Conditions
- Connection timeout errors
- Query execution failures
- Migration errors
- Pool exhaustion

## Error Patterns & Solutions

### Pattern: Connection Timeout
\`\`\`python
# Detection
if "connection timeout" in str(error).lower():
    # Solution
    solutions = [
        "1. Check DATABASE_URL in .env",
        "2. Verify database server is running",
        "3. Check firewall/network settings",
        "4. Increase connection timeout in config"
    ]
\`\`\`

### Pattern: Pool Exhaustion
\`\`\`python
# Detection
if "too many connections" in str(error).lower():
    # Solution
    solutions = [
        "1. Increase pool_size in database config",
        "2. Add connection recycling",
        "3. Check for connection leaks",
        "4. Implement connection pooling (PgBouncer)"
    ]
\`\`\`
```

### Category 5: Testing Skills
**Purpose:** Generate test cases, mocks, fixtures

```markdown
# Example: Test Generator Skill

## Purpose
Generate comprehensive test suites for components/functions

## Inputs Required
- Function/Component to test
- Test framework (pytest, jest, etc.)
- Coverage requirements
- Mock requirements

## Code Templates

### Pytest Test Template
\`\`\`python
import pytest
from unittest.mock import Mock, patch
from {{module}} import {{function_or_class}}

class Test{{FunctionOrClass}}:
    """Test suite for {{function_or_class}}"""

    @pytest.fixture
    def {{fixture_name}}(self):
        """Setup test fixture"""
        return {{fixture_value}}

    def test_{{function}}_success(self, {{fixture_name}}):
        """Test successful execution"""
        # Arrange
        {{arrange}}

        # Act
        result = {{function_or_class}}({{args}})

        # Assert
        assert result == {{expected}}

    def test_{{function}}_failure(self, {{fixture_name}}):
        """Test failure case"""
        # Arrange
        {{arrange_failure}}

        # Act & Assert
        with pytest.raises({{ExpectedException}}):
            {{function_or_class}}({{invalid_args}})

    @patch('{{module}}.{{dependency}}')
    def test_{{function}}_with_mock(self, mock_{{dependency}}):
        """Test with mocked dependency"""
        # Arrange
        mock_{{dependency}}.return_value = {{mock_return}}

        # Act
        result = {{function_or_class}}({{args}})

        # Assert
        mock_{{dependency}}.assert_called_once_with({{expected_args}})
        assert result == {{expected}}
\`\`\`
```

---

## Skill Generation Process

When user asks for a new skill, follow these steps:

### Step 1: Analyze Requirements
```
- What problem does this skill solve?
- What inputs are needed?
- What outputs are expected?
- What errors might occur?
- What templates/code are needed?
```

### Step 2: Choose Skill Category
```
- Code Generator → For creating files/components
- API/Backend → For server-side operations
- DevOps → For infrastructure/deployment
- Error Handler → For handling specific errors
- Testing → For generating tests
- Workflow → For multi-step processes
- Integration → For connecting services
```

### Step 3: Generate Skill Structure
```bash
mkdir -p .claude/skills/<skill-name>
# Create SKILL.md with full definition
# Add templates/ if code generation needed
# Add scripts/ if automation needed
# Add examples/ for usage clarity
```

### Step 4: Write SKILL.md
```
1. Clear purpose statement
2. Specific trigger conditions
3. Required inputs list
4. Step-by-step execution
5. Code templates with placeholders
6. Error handling strategies
7. Real-world examples
```

### Step 5: Test & Validate
```
1. Verify skill triggers correctly
2. Test all code templates
3. Validate error handling
4. Document edge cases
```

---

## Script Templates for Skills

### Bash Script Template
```bash
#!/bin/bash
set -euo pipefail

# ============================================
# {{SCRIPT_NAME}}
# Purpose: {{PURPOSE}}
# Usage: ./{{script_name}}.sh [options]
# ============================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# Default values
{{DEFAULT_VARS}}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            echo "Usage: $0 [options]"
            echo "Options:"
            echo "  -h, --help     Show this help message"
            {{HELP_OPTIONS}}
            exit 0
            ;;
        {{OPTION_CASES}}
        *)
            log_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

# Main execution
main() {
    log_info "Starting {{SCRIPT_NAME}}..."

    {{MAIN_LOGIC}}

    log_info "{{SCRIPT_NAME}} completed successfully!"
}

# Run main function
main "$@"
```

### Python Script Template
```python
#!/usr/bin/env python3
"""
{{SCRIPT_NAME}}
Purpose: {{PURPOSE}}
Usage: python {{script_name}}.py [options]
"""

import argparse
import logging
import sys
from pathlib import Path
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='{{PURPOSE}}',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    {{ARGUMENT_DEFINITIONS}}
    return parser.parse_args()


def main() -> int:
    """Main entry point."""
    args = parse_args()

    try:
        logger.info("Starting {{SCRIPT_NAME}}...")

        {{MAIN_LOGIC}}

        logger.info("{{SCRIPT_NAME}} completed successfully!")
        return 0

    except Exception as e:
        logger.error(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
```

### PowerShell Script Template
```powershell
#Requires -Version 5.1
<#
.SYNOPSIS
    {{SCRIPT_NAME}}
.DESCRIPTION
    {{PURPOSE}}
.PARAMETER {{ParamName}}
    {{ParamDescription}}
.EXAMPLE
    .\{{script_name}}.ps1 -{{ParamName}} "value"
#>

[CmdletBinding()]
param(
    {{PARAMETER_DEFINITIONS}}
)

# Error handling
$ErrorActionPreference = "Stop"

function Write-Log {
    param(
        [string]$Message,
        [ValidateSet("INFO", "WARN", "ERROR")]
        [string]$Level = "INFO"
    )

    $color = switch ($Level) {
        "INFO"  { "Green" }
        "WARN"  { "Yellow" }
        "ERROR" { "Red" }
    }

    Write-Host "[$Level] $Message" -ForegroundColor $color
}

function Main {
    Write-Log "Starting {{SCRIPT_NAME}}..."

    try {
        {{MAIN_LOGIC}}

        Write-Log "{{SCRIPT_NAME}} completed successfully!"
    }
    catch {
        Write-Log "Error: $_" -Level "ERROR"
        exit 1
    }
}

# Run main
Main
```

---

## Integration Patterns

### MCP Tool Integration
```python
# MCP Tool Template for Skills
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("{{skill-name}}")

@server.tool()
async def {{tool_name}}({{parameters}}) -> list[TextContent]:
    """{{Tool description}}"""

    # Validate inputs
    {{validation}}

    # Execute logic
    {{execution}}

    # Return result
    return [TextContent(type="text", text={{result}})]
```

### Claude Command Integration
```markdown
# .claude/commands/{{command-name}}.md

## Command: /{{command-name}}

### Purpose
{{Purpose description}}

### Usage
\`\`\`
/{{command-name}} [arguments]
\`\`\`

### Arguments
- `arg1`: {{description}}
- `arg2`: {{description}}

### Execution
1. {{Step 1}}
2. {{Step 2}}
3. {{Step 3}}

### Output
{{Expected output format}}
```

---

## Best Practices for Skill Creation

### DO:
- Make skills focused and single-purpose
- Include comprehensive error handling
- Provide multiple code templates for variations
- Add real-world examples
- Document all placeholders clearly
- Include validation logic

### DON'T:
- Create overly complex multi-purpose skills
- Hardcode values (use placeholders)
- Ignore error scenarios
- Skip documentation
- Forget to handle edge cases

---

## Quick Skill Generation Command

When user says "Create a skill for X", respond with:

```
I'll create a new skill for you. Let me:

1. Analyze what "X" needs
2. Choose the right category
3. Generate SKILL.md with:
   - Clear purpose
   - Trigger conditions
   - Input requirements
   - Execution steps
   - Code templates
   - Error handling
   - Examples

Creating skill at: .claude/skills/<skill-name>/SKILL.md
```

Then generate the complete skill following this master template.

---

## Version
- **Version**: 1.0.0
- **Created**: 2025-12-29
- **Purpose**: Master skill for generating new skills on demand
