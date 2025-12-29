# Phase 4: Local Kubernetes Deployment

## Overview

Deploy the AI-powered todo chatbot on a local Kubernetes cluster using Minikube.

## Status

**Phase Status**: Not Started

## Technology Stack

- **Containerization**: Docker
- **Orchestration**: Kubernetes (Minikube)
- **Package Manager**: Helm
- **AI DevOps**: kubectl-ai, kagent

## Deliverables

1. Dockerfiles for frontend and backend
2. Helm charts for deployment
3. Minikube deployment
4. AI DevOps demonstration

## Project Structure

```
Phase_4/
├── .claude/          # Claude Code configuration
├── .specify/         # SpecKit Plus configuration
├── specs/            # Feature specifications
├── history/          # Development history
├── docker/           # Dockerfiles (TODO)
├── helm/             # Helm charts (TODO)
├── k8s/              # K8s manifests (TODO)
└── README.md
```

## Getting Started

Phase 4 has not been implemented yet. Check specs/spec.md for requirements.

## Prerequisites

- Phase 3 completed
- Docker Desktop installed
- Minikube installed
- Helm installed
- kubectl-ai (optional)

## Quick Start (after implementation)

```bash
# Start Minikube
minikube start

# Build and load images
docker build -t todo-frontend:latest ./docker/frontend
docker build -t todo-backend:latest ./docker/backend
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# Deploy with Helm
helm install todo-app ./helm/todo-app

# Verify
kubectl get pods
kubectl get svc
```

## Documentation

- [Specification](specs/spec.md)
- [Claude Code Rules](CLAUDE.md)
- [Constitution](.specify/memory/constitution.md)
