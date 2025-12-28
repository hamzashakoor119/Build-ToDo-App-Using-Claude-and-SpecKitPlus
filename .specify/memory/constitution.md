# Evolution of Todo - Hackathon II Constitution

## Project Overview

**Project Name**: Evolution of Todo - Spec-Driven Cloud-Native AI System
**Purpose**: Master the art of building applications iteratively from console app to fully-featured cloud-native AI chatbot
**Goal**: Transform from "syntax writer" to "system architect" using AI-native spec-driven development

## Core Principles

### I. Spec-Driven Development (MANDATORY)

**All code must be generated from specifications. Manual coding is prohibited.**

- Every feature MUST have a written specification before implementation
- Specifications live in `/specs` directory, organized by phase and feature type
- Cannot write code manually - must refine specs until Claude Code generates correct output
- Specifications must include:
  - User stories and acceptance criteria
  - API contracts and data models
  - UI/UX requirements
  - Error handling and edge cases
- Use GitHub Spec-Kit Plus for specification management
- Reference specs using `@specs/path/to/spec.md` syntax

**Constraint**: If code exists without a spec, it is non-compliant and must be removed or documented retroactively.

### II. Prompt History Records (PHR) - Required for Every Interaction

**Every user interaction must be captured in a Prompt History Record.**

- Create PHR after EVERY user input that involves:
  - Implementation work (code changes, new features)
  - Planning/architecture discussions
  - Debugging sessions
  - Spec/task/plan creation
  - Multi-step workflows

**PHR Creation Process**:
1. Detect stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general
2. Generate descriptive title (3-7 words) and create slug for filename
3. Route appropriately:
   - Constitution → `history/prompts/constitution/`
   - Feature stages → `history/prompts/<feature-name>/`
   - General → `history/prompts/general/`
4. Use agent-native flow (no shell) to read template and fill ALL placeholders
5. Include complete user input (not truncated) and representative assistant output
6. Validate: No placeholders, complete content, correct path

**Skip PHR only for**: `/sp.phr` command itself

### III. Architecture Decision Records (ADR) - Intelligent Suggestions

**Significant architectural decisions must be documented, not auto-created.**

**Three-Part Significance Test**:
- Impact: Does this have long-term consequences? (framework, data model, API, security, platform)
- Alternatives: Were multiple viable options considered?
- Scope: Is this cross-cutting and influences system design?

**If ALL three are true**:
- Suggest: "📋 Architectural decision detected: [brief-description]. Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`"
- Wait for user consent - NEVER auto-create ADRs
- Group related decisions (stacks, authentication, deployment) into one ADR when appropriate
- ADRs stored in `history/adr/`

**When ADR suggestions typically occur**: During `/sp.plan` and `/sp.tasks` execution

### IV. Technology Stack Compliance

**Each phase has a mandated technology stack that must be followed.**

**Phase I: In-Memory Python Console App**
- Language: Python 3.13+
- Package Manager: UV
- Tools: Claude Code, Spec-Kit Plus
- Features: Basic Level (Add, Delete, Update, View, Mark Complete)

**Phase II: Full-Stack Web Application**
- Frontend: Next.js 16+ (App Router), TypeScript, Tailwind CSS
- Backend: Python FastAPI
- ORM: SQLModel
- Database: Neon Serverless PostgreSQL
- Authentication: Better Auth with JWT
- Features: All Basic Level + User Authentication

**Phase III: AI-Powered Todo Chatbot**
- Frontend UI: OpenAI ChatKit
- AI Framework: OpenAI Agents SDK
- MCP Server: Official MCP SDK (Python)
- Architecture: Stateless chat endpoint with database-persisted conversation state
- Features: All Basic Level via natural language + MCP tools

**Phase IV: Local Kubernetes Deployment**
- Containerization: Docker (Docker Desktop)
- Docker AI: Gordon (if available in region)
- Orchestration: Kubernetes (Minikube)
- Package Manager: Helm Charts
- AI DevOps: kubectl-ai, kagent
- Features: Deployed chatbot on local Minikube

**Phase V: Advanced Cloud Deployment**
- Advanced Features: Recurring Tasks, Due Dates & Reminders, Priorities, Tags, Search, Filter, Sort
- Event Streaming: Kafka on Redpanda Cloud (Serverless tier)
- Distributed Runtime: Dapr (Pub/Sub, State, Bindings, Secrets, Service Invocation)
- Cloud Platform: DigitalOcean Kubernetes (DOKS) OR Google Cloud (GKE) OR Azure (AKS)
- CI/CD: GitHub Actions
- Monitoring: Configured logging and observability

**No substitutions allowed** without documented architectural justification.

### V. Test-First Development (NON-NEGOTIABLE)

**All code must be tested. Tests are written before implementation.**

- Follow Red-Green-Refactor cycle:
  1. Write test (Red - fails)
  2. Implement minimum code to pass (Green)
  3. Refactor for quality
- Tests must cover:
  - Unit tests for all functions/methods
  - Integration tests for API endpoints
  - End-to-end tests for critical user flows
  - MCP tool tests (Phase III+)
- Test files co-located with source code or in `/tests` directory
- All tests must pass before phase submission

### VI. Clean Code and Simplicity

**Code must be simple, readable, and maintainable.**

- Follow clean code principles
- Proper project structure for each technology
- No over-engineering - implement only what's required
- Use clear, descriptive names for variables, functions, classes
- Comment only where logic isn't self-evident
- No hardcoded secrets or tokens - use `.env` and secret management
- Prefer smallest viable diff - don't refactor unrelated code
- Code references with `start:end:path` format

### VII. Human as Tool Strategy

**Invoke user for clarification when facing ambiguity or significant decisions.**

**Invocation Triggers**:
1. **Ambiguous Requirements**: Ask 2-3 targeted clarifying questions
2. **Unforeseen Dependencies**: Surface dependencies and ask for prioritization
3. **Architectural Uncertainty**: Present options with tradeoffs, get user preference
4. **Completion Checkpoint**: Summarize completed work and confirm next steps

**Do not invent**: APIs, data contracts, or business logic without user input.

### VIII. Monorepo Organization (Phase II+)

**Full-stack phases use monorepo structure with organized specs.**

```
hackathon-todo/
├── .specify/              # Spec-Kit Plus configuration
├── specs/                 # Organized specifications
│   ├── features/         # Feature specs
│   ├── api/              # API and MCP specs
│   ├── database/         # Schema specs
│   └── ui/               # UI component specs
├── history/
│   ├── prompts/          # PHR records
│   └── adr/              # Architecture Decision Records
├── frontend/             # Next.js application
│   └── CLAUDE.md         # Frontend-specific guidance
├── backend/              # FastAPI application
│   └── CLAUDE.md         # Backend-specific guidance
├── CLAUDE.md             # Root Claude Code instructions
└── README.md             # User documentation
```

**CLAUDE.md Hierarchy**:
- Root: Project overview, spec structure, development workflow
- Frontend: Stack, patterns, component structure, API client usage
- Backend: Stack, project structure, API conventions, database usage

## Development Workflow

### Feature Implementation Flow

1. **Specification Phase**
   - Write spec in `/specs/features/<feature-name>.md`
   - Include user stories, acceptance criteria, API contracts
   - Review and refine spec with user

2. **Planning Phase** (if complex)
   - Run `/sp.plan` to generate implementation plan
   - Document architectural decisions
   - Suggest ADRs for significant decisions

3. **Task Breakdown** (if complex)
   - Run `/sp.tasks` to generate testable tasks
   - Tasks must reference code precisely
   - Include test cases for each task

4. **Implementation Phase**
   - Use Claude Code to generate implementation from specs
   - Follow Test-First Development
   - Create PHR for implementation session
   - Refine spec if Claude Code output is incorrect

5. **Verification Phase**
   - Run all tests
   - Verify acceptance criteria met
   - Test manually if needed

6. **Documentation Phase**
   - Update README with setup instructions
   - Document API endpoints
   - Document deployment procedures

### Git Workflow

**Commit Requirements**:
- ONLY create commits when requested by user
- Follow Git Safety Protocol (see CLAUDE.md)
- NEVER skip hooks or force push to main/master without explicit user request
- Commit message format:
  ```
  [Descriptive message focusing on "why" not "what"]

  🤖 Generated with [Claude Code](https://claude.com/claude-code)

  Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
  ```

**Branch Strategy** (if used):
- Feature branches for each phase
- Main branch protected
- Create PRs for phase completions

### Pull Request Requirements

**When user requests PR creation**:
1. Understand full commit history from branch divergence
2. Analyze all changes (not just latest commit)
3. Draft comprehensive PR summary with test plan
4. Push to remote with `-u` flag if needed
5. Use `gh pr create` with proper template
6. Include documentation updates and deployment notes

## Quality Standards

### Code Quality

- **Security**: No vulnerabilities (XSS, SQL injection, command injection, OWASP Top 10)
- **Performance**: Efficient queries, proper indexing, optimized assets
- **Scalability**: Stateless services, horizontal scaling support (Phase IV+)
- **Observability**: Structured logging, error tracking, monitoring (Phase V)
- **Documentation**: README, API docs, setup instructions

### API Standards (Phase II+)

- RESTful conventions
- Consistent error responses with HTTP status codes
- JSON request/response format
- API versioning if needed
- Proper authentication and authorization
- Input validation and sanitization

### MCP Tools Standards (Phase III+)

- Stateless tools that store state in database
- Clear parameter definitions with types and descriptions
- Consistent return format with status and data
- Error handling with meaningful messages
- Tool naming: verb_noun format (e.g., `add_task`, `list_tasks`)

### Database Standards

- SQLModel for all database operations
- Proper foreign key relationships
- Indexes on frequently queried fields
- Migration scripts for schema changes
- Connection pooling
- Environment-based connection strings

### Deployment Standards (Phase IV+)

**Local Kubernetes (Minikube)**:
- Dockerfiles for all services
- Helm charts for deployment
- ConfigMaps for configuration
- Secrets for sensitive data
- Resource limits defined

**Cloud Kubernetes (DOKS/GKE/AKS)**:
- Production-grade Helm charts
- Horizontal Pod Autoscaling
- Ingress configuration
- TLS certificates
- Monitoring and logging configured

**Dapr Integration (Phase V)**:
- Component specifications in YAML
- Pub/Sub for event-driven communication
- State management for conversation state
- Bindings for scheduled tasks (cron)
- Secrets management for credentials

## Constraints and Non-Goals

### Constraints

- **No Manual Coding**: All code must be generated from specs via Claude Code
- **No Skipping Phases**: Must complete phases in order (I → II → III → IV → V)
- **WSL 2 Required**: Windows users must use WSL 2 for development
- **Individual Work**: No team submissions - individual hackathon
- **Technology Stack Fixed**: Cannot substitute core technologies without justification

### Non-Goals

- **No Over-Engineering**: Don't add features beyond phase requirements
- **No Premature Optimization**: Optimize only when needed
- **No Unrelated Refactoring**: Change only code related to current feature
- **No Auto-Documentation**: Don't create docs unless explicitly requested

## Success Criteria

### Phase Completion Criteria

**Phase I: In-Memory Python Console App**
- [ ] Console app with all 5 Basic Level features
- [ ] Spec files in `/specs`
- [ ] Clean Python project structure
- [ ] Tests passing
- [ ] GitHub repository with proper structure

**Phase II: Full-Stack Web Application**
- [ ] Responsive web UI with all Basic Level features
- [ ] RESTful API with proper endpoints
- [ ] Better Auth authentication working
- [ ] JWT token verification
- [ ] Neon DB integrated
- [ ] Deployed on Vercel (frontend) and accessible backend
- [ ] Monorepo structure with specs

**Phase III: AI-Powered Todo Chatbot**
- [ ] ChatKit UI integrated
- [ ] OpenAI Agents SDK functional
- [ ] MCP server with all 5 tools (add, list, complete, delete, update)
- [ ] Stateless architecture with database-persisted conversations
- [ ] Natural language task management working
- [ ] OpenAI domain allowlist configured

**Phase IV: Local Kubernetes Deployment**
- [ ] Docker containers for frontend and backend
- [ ] Helm charts created
- [ ] Deployed successfully on Minikube
- [ ] kubectl-ai and/or kagent used for K8s operations
- [ ] Documentation for local setup

**Phase V: Advanced Cloud Deployment**
- [ ] All Advanced Level features implemented (Recurring Tasks, Due Dates, Reminders)
- [ ] All Intermediate Level features implemented (Priorities, Tags, Search, Filter, Sort)
- [ ] Kafka integration with Redpanda Cloud
- [ ] Dapr components configured (Pub/Sub, State, Bindings, Secrets, Service Invocation)
- [ ] Deployed on cloud Kubernetes (DOKS/GKE/AKS)
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Monitoring and logging configured
- [ ] Event-driven architecture functional

### Bonus Criteria (Optional)

- [ ] **Reusable Intelligence**: Create and use Claude Code Subagents and Agent Skills
- [ ] **Cloud-Native Blueprints**: Create and use blueprints via Agent Skills
- [ ] **Multi-language Support**: Support Urdu in chatbot
- [ ] **Voice Commands**: Add voice input for todo commands

### Repository Structure Requirements

**Repository Must Contain**:
- Constitution file (this document)
- `/specs` folder with all specification files organized by type
- `/history/prompts` folder with PHR records
- `/history/adr` folder with ADRs (if any)
- `/src` or phase-appropriate source folders
- `README.md` with comprehensive setup instructions
- `CLAUDE.md` with Claude Code instructions and development guidance
- Working code for completed phases
- Tests for all implemented features

## Governance

### Constitution Authority

- This constitution supersedes all other development practices
- All development must comply with principles outlined here
- All code reviews must verify constitutional compliance
- Complexity must be justified against simplicity principle

### Amendment Process

- Amendments require:
  1. Clear documentation of reason for change
  2. User approval
  3. Migration plan for existing code (if applicable)
  4. ADR documenting the constitutional change

### Compliance Verification

- Every PR/commit must align with constitutional principles
- PHR creation is mandatory - absence is non-compliance
- ADR suggestions for significant decisions are required
- Spec-first approach is non-negotiable

### Runtime Guidance

- Use `CLAUDE.md` files for runtime development guidance
- Constitution provides principles, CLAUDE.md provides implementation patterns
- When conflict arises, constitution takes precedence

## Key Success Metrics

**Technical Excellence**:
- All phases completed with working deployments
- All tests passing
- No security vulnerabilities
- Clean, maintainable code structure
- Comprehensive documentation

**Spec-Driven Development**:
- Every feature has corresponding spec
- PHR created for all development sessions
- ADRs created for significant decisions
- Clear traceability from spec to implementation

**Learning Outcomes**:
- Mastery of Claude Code and Spec-Kit Plus
- Understanding of full-stack development with modern tools
- Experience with AI agent development (MCP, OpenAI Agents SDK)
- Proficiency in cloud-native technologies (Kubernetes, Helm, Dapr, Kafka)
- AIOps experience with kubectl-ai and kagent
- Evolution from "syntax writer" to "system architect"

---

**Version**: 1.0.0
**Ratified**: 2025-12-26
**Last Amended**: 2025-12-26

**Remember**: The future of software development is AI-native and spec-driven. Your role is evolving from "syntax writer" to "system architect." This project will teach you the Architecture of Intelligence.

May your specs be clear and your code be clean! 🚀
