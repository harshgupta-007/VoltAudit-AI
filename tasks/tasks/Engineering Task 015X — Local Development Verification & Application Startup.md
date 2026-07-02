# Engineering Task 015X — Local Development Verification & Application Startup

## Role

You are a Principal Release Engineer at Google responsible for validating, launching, and verifying production-grade AI applications before release.

You are working on VoltAudit AI.

The project has successfully completed all engineering milestones, including:

- Enterprise Architecture
- AI Workforce
- MCP Platform
- Antigravity Skills
- ADK Platform
- Business Agents
- FastAPI Application
- Streamlit Frontend
- Security Hardening
- Production Deployment
- CI/CD

Your responsibility is NOT to modify the architecture.

Your responsibility is to verify that the repository can be executed successfully on a local development machine.

---

# Repository Intelligence Phase (Mandatory)

Before generating any commands:

1. Inspect the complete repository.
2. Identify every executable component.
3. Inspect every `pyproject.toml`.
4. Inspect every `requirements.txt`.
5. Inspect every `Dockerfile`.
6. Inspect `docker-compose.yml`.
7. Inspect `.env.example`.
8. Inspect startup scripts.
9. Inspect Makefiles.
10. Inspect shell scripts.
11. Inspect package.json files.
12. Inspect Streamlit entrypoints.
13. Inspect FastAPI entrypoints.
14. Inspect ADK entrypoints.
15. Inspect MCP entrypoints.

Do NOT assume anything.

Generate commands only after repository inspection.

---

# Objective

Determine the correct procedure for running VoltAudit AI locally.

Generate only commands that are valid for THIS repository.

Do not invent commands.

Do not assume directory structures.

Verify everything from the repository.

---

# Deliverables

## 1. Repository Startup Report

Explain:

- executable components
- startup dependencies
- startup order
- required environment variables
- required services

---

## 2. Local Development Setup

Generate exact commands to:

- create virtual environments
- install dependencies
- configure environment variables
- install frontend dependencies
- initialize databases (if required)

---

## 3. Correct Startup Order

Determine the correct startup sequence.

For example:

Environment

↓

Database

↓

MCP

↓

ADK

↓

FastAPI

↓

Frontend

or another order if required.

Explain why.

---

## 4. Exact Run Commands

Generate exact commands for:

Backend

MCP

ADK

Frontend

Docker

Docker Compose

Only generate commands that actually match the repository.

---

## 5. Health Checks

For every service provide:

- expected startup logs
- expected URLs
- health endpoints
- readiness endpoints

Explain how to verify each component is healthy.

---

## 6. End-to-End Verification

Generate an end-to-end validation procedure.

Include:

- upload invoice
- trigger AI workflow
- verify Coordinator Agent
- verify Specialist Agents
- verify MCP Tool usage
- verify FastAPI
- verify Frontend
- verify generated audit report

---

## 7. Troubleshooting Guide

Identify common startup failures.

For each failure provide:

- root cause
- diagnosis
- resolution

Include:

- missing dependencies
- missing API keys
- missing environment variables
- import failures
- port conflicts
- Docker issues
- Streamlit issues
- FastAPI issues
- MCP issues
- ADK issues

---

## 8. Startup Validation Checklist

Generate a checklist confirming:

□ Backend running

□ Frontend running

□ MCP connected

□ ADK initialized

□ Agents registered

□ Skills loaded

□ APIs reachable

□ Dashboard accessible

□ End-to-end workflow successful

---

# Constraints

Do NOT modify code.

Do NOT redesign architecture.

Do NOT generate placeholder commands.

Every command must be verified against the repository before being generated.

If any executable component is missing, clearly identify it and explain what is missing instead of guessing.

---

# Acceptance Criteria

The task is complete when:

- the repository has been inspected,
- every executable component has been identified,
- exact startup commands have been generated,
- startup order has been verified,
- health checks are documented,
- an end-to-end verification procedure has been produced,
- the application can be confidently executed on a local development machine.
