# Phase 4: Local Kubernetes Deployment - Claude Code Rules

## Project Context

**Phase**: 4 of 5 - Local Kubernetes Deployment
**Scope**: Deploy the AI chatbot on local Minikube cluster
**Status**: Self-contained, portable project folder

## Technology Stack (Phase 4 Specific)

- **Containerization**: Docker (Docker Desktop)
- **Docker AI**: Gordon (if available)
- **Orchestration**: Kubernetes (Minikube)
- **Package Manager**: Helm Charts
- **AI DevOps**: kubectl-ai, kagent

## Project Structure

```
Phase_4/
├── .claude/              # Claude Code configuration
│   ├── commands/         # Slash commands
│   └── skills/           # K8s-specific skills
├── .specify/             # SpecKit Plus configuration
│   ├── memory/           # Constitution and session state
│   └── templates/        # Spec, plan, task templates
├── specs/                # Feature specifications
│   ├── checklists/       # Requirements checklists
│   ├── contracts/        # K8s resource contracts
│   ├── spec.md           # Main specification
│   ├── plan.md           # Implementation plan
│   └── tasks.md          # Task breakdown
├── history/              # Development history
│   ├── prompts/          # Prompt History Records (PHRs)
│   └── adr/              # Architecture Decision Records
├── docker/               # Dockerfiles
│   ├── frontend/         # Frontend Dockerfile
│   └── backend/          # Backend Dockerfile
├── helm/                 # Helm charts
│   └── todo-app/         # Main chart
├── k8s/                  # Raw K8s manifests (optional)
└── README.md             # Phase documentation
```

## Core Deliverables

1. **Docker Images**: Frontend and backend containerized
2. **Helm Charts**: Parameterized deployment
3. **Minikube Deployment**: Running cluster
4. **AI DevOps**: kubectl-ai/kagent usage demonstrated

## Docker Standards

```dockerfile
# Multi-stage builds for smaller images
# Non-root user for security
# Environment-based configuration
# Health checks defined
```

## Helm Chart Structure

```yaml
todo-app/
├── Chart.yaml
├── values.yaml
├── templates/
│   ├── deployment-frontend.yaml
│   ├── deployment-backend.yaml
│   ├── service-frontend.yaml
│   ├── service-backend.yaml
│   ├── configmap.yaml
│   ├── secret.yaml
│   └── ingress.yaml
```

## Development Guidelines

### Spec-Driven Development
- All infrastructure as code from specs
- K8s resources have contracts
- Use `/sp.specify`, `/sp.plan`, `/sp.tasks` commands

### PHR Requirements
After completing tasks, create PHR in `history/prompts/`:
- Stage: spec | plan | tasks | red | green | refactor
- Route: `history/prompts/<ID>-<slug>.<stage>.prompt.md`

### K8s Standards
- Resource limits defined
- ConfigMaps for configuration
- Secrets for sensitive data
- Health probes configured
- Labels and annotations

## Commands Reference

```bash
# Start Minikube
minikube start

# Build images
docker build -t todo-frontend:latest ./docker/frontend
docker build -t todo-backend:latest ./docker/backend

# Load images to Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# Deploy with Helm
helm install todo-app ./helm/todo-app

# Check status
kubectl get pods
kubectl get svc

# AI DevOps
kubectl-ai "scale the frontend to 3 replicas"
kagent apply deployment-changes
```

## Success Criteria

- [ ] Docker containers for frontend and backend
- [ ] Helm charts created and tested
- [ ] Successfully deployed on Minikube
- [ ] kubectl-ai and/or kagent usage demonstrated
- [ ] Documentation for local setup complete

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
