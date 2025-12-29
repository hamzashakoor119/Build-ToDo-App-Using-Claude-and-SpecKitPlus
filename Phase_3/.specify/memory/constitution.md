# Phase 3 Constitution: AI-Powered Todo Chatbot

## Project Overview

**Phase**: 3 - AI-Powered Todo Chatbot
**Purpose**: Enable natural language task management via AI chatbot
**Technology**: OpenAI ChatKit + Agents SDK + MCP

## Core Principles

### I. Spec-Driven Development (MANDATORY)
- All code must be generated from specifications
- MCP tools require contracts
- No manual coding without spec

### II. Stateless Architecture
- Chat endpoint is stateless
- Conversation state persisted in database
- MCP tools store state in database

### III. AI-First Design
- Natural language as primary interface
- AI interprets user intent
- Tools execute specific actions

## Technology Stack

| Component | Technology |
|-----------|------------|
| UI | OpenAI ChatKit |
| AI Framework | OpenAI Agents SDK |
| MCP Server | Official MCP SDK (Python) |
| Backend | FastAPI |
| Database | Neon PostgreSQL |

## Features Scope

### In Scope
- All Basic Level features via natural language
- MCP tools for CRUD operations
- Conversation state persistence
- ChatKit integration

### Out of Scope
- Voice commands
- Multi-language support
- Kubernetes deployment
- Advanced task features

## MCP Tool Standards

- Stateless tools
- Database state persistence
- Clear parameter types
- Consistent error handling
- Tool naming: verb_noun format

## Quality Standards

- All MCP tools tested
- Natural language understanding accurate
- Conversation context maintained
- Error messages user-friendly

## Success Criteria

- [ ] ChatKit UI working
- [ ] OpenAI Agents functional
- [ ] All 5 MCP tools implemented
- [ ] Stateless architecture
- [ ] Natural language management
- [ ] Documentation complete

---
**Version**: 1.0.0
**Phase**: 3 of 5
**Ratified**: 2025-12-29
