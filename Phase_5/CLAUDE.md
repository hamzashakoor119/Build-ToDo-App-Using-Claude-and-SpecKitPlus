# Phase 5: Advanced Cloud Deployment - Claude Code Rules

## Project Context

**Phase**: 5 of 5 - Advanced Cloud Deployment
**Scope**: Production-grade cloud deployment with advanced features
**Status**: Self-contained, portable project folder

## Technology Stack (Phase 5 Specific)

### Advanced Features
- Recurring Tasks
- Due Dates & Reminders
- Priorities, Tags
- Search, Filter, Sort

### Event Streaming
- **Platform**: Kafka on Redpanda Cloud (Serverless tier)

### Distributed Runtime
- **Framework**: Dapr
- **Components**: Pub/Sub, State, Bindings, Secrets, Service Invocation

### Cloud Platform (choose one)
- DigitalOcean Kubernetes (DOKS)
- Google Cloud (GKE)
- Azure (AKS)

### CI/CD
- GitHub Actions

## Project Structure

```
Phase_5/
├── .claude/              # Claude Code configuration
│   ├── commands/         # Slash commands
│   └── skills/           # Cloud-specific skills
├── .specify/             # SpecKit Plus configuration
│   ├── memory/           # Constitution and session state
│   └── templates/        # Spec, plan, task templates
├── specs/                # Feature specifications
│   ├── checklists/       # Requirements checklists
│   ├── contracts/        # API and event contracts
│   ├── spec.md           # Main specification
│   ├── plan.md           # Implementation plan
│   └── tasks.md          # Task breakdown
├── history/              # Development history
│   ├── prompts/          # Prompt History Records (PHRs)
│   └── adr/              # Architecture Decision Records
├── helm/                 # Production Helm charts
├── dapr/                 # Dapr components
│   ├── pubsub.yaml       # Pub/Sub config
│   ├── statestore.yaml   # State management
│   └── bindings.yaml     # Cron bindings
├── .github/              # GitHub Actions
│   └── workflows/
│       └── deploy.yaml
└── README.md             # Phase documentation
```

## Advanced Features

### Intermediate Level
- **Priorities**: High, Medium, Low
- **Tags**: Custom labels for tasks
- **Search**: Full-text search
- **Filter**: By status, priority, tags
- **Sort**: By date, priority, title

### Advanced Level
- **Recurring Tasks**: Daily, weekly, monthly
- **Due Dates**: Calendar integration
- **Reminders**: Notification system

## Dapr Components

```yaml
# Pub/Sub (Kafka on Redpanda)
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: task-events
spec:
  type: pubsub.kafka
  metadata:
  - name: brokers
    secretKeyRef: kafka-brokers

# State Store
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: conversation-state
spec:
  type: state.postgresql

# Bindings (Cron for reminders)
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminder-cron
spec:
  type: bindings.cron
```

## Event-Driven Architecture

```
Task Created → Kafka → Notification Service
Task Due Soon → Cron Binding → Reminder Publisher
Recurring Task → Scheduled Trigger → Task Generator
```

## Development Guidelines

### Spec-Driven Development
- All infrastructure from specifications
- Event schemas defined as contracts
- Use `/sp.specify`, `/sp.plan`, `/sp.tasks` commands

### PHR Requirements
After completing tasks, create PHR in `history/prompts/`:
- Stage: spec | plan | tasks | red | green | refactor
- Route: `history/prompts/<ID>-<slug>.<stage>.prompt.md`

### Cloud Standards
- Production-grade Helm charts
- HPA for auto-scaling
- Ingress with TLS
- Monitoring configured
- Secrets in cloud secret manager

## CI/CD Pipeline

```yaml
# .github/workflows/deploy.yaml
name: Deploy to Cloud
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - Build Docker images
      - Push to container registry
      - Update Helm values
      - Deploy to Kubernetes
      - Run smoke tests
```

## Success Criteria

- [ ] All Advanced Level features implemented
- [ ] All Intermediate Level features implemented
- [ ] Kafka integration with Redpanda Cloud
- [ ] Dapr components configured
- [ ] Deployed on cloud Kubernetes
- [ ] CI/CD pipeline functional
- [ ] Monitoring and logging configured
- [ ] Event-driven architecture working

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
