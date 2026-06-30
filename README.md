# VoltAudit AI ⚡🔍

[![CI](https://github.com/voltaudit-ai/voltaudit/actions/workflows/ci.yml/badge.svg)](https://github.com/voltaudit-ai/voltaudit/actions/workflows/ci.yml)
[![Semgrep Security](https://img.shields.io/badge/security-semgrep-blue.svg)](https://semgrep.dev/)
[![Pre-Commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![License: Proprietary](https://img.shields.io/badge/License-Proprietary-red.svg)](#)

Enterprise AI Workforce for Intelligent Invoice Auditing. VoltAudit AI automatically ingests, normalizes, analyzes, and audits corporate invoices against contractual terms, tax regulations, and internal expenditure compliance policies.

---

## 🏗️ Repository Architecture

This repository is constructed following **Spec-Driven Development** and **Agentic Engineering** principles. The folder layout is organized as follows:

```
.
├── .agents/                    # Custom agent configuration templates & project guidelines
├── .github/workflows/          # CI/CD and automation definitions
├── .semgrep/                   # Custom Semgrep security policy rules
├── docs/                       # High-level architecture and developer onboarding guides
├── specs/                      # Product and technical specifications
├── tasks/                      # Sprint tasks backlog and templates
├── backend/                    # Core Python API (FastAPI, SQLModel)
├── frontend/                   # UI dashboard (React, TypeScript, Vite)
├── agents/                     # AI agents and LLM orchestration layer
├── mcp/                        # Model Context Protocol (MCP) servers and tools
├── tests/                      # Multi-layer testing suite (unit, integration, e2e)
├── deploy/                     # Docker containers, orchestrations, and deployment scripts
└── antigravity-skills/         # Pre-packaged agent skills
```

---

## 🚀 Getting Started

To onboard as a developer, follow these steps:

1. **Read the Documentation First:**
   - [Developer Onboarding](file:///d:/Self_Learning/my-first-project-5-days-google-course/Capstone_Project/docs/onboarding.md) — Step-by-step developer setup.
   - [Engineering Standards](file:///d:/Self_Learning/my-first-project-5-days-google-course/Capstone_Project/docs/engineering_standards.md) — Code design and architecture invariants.
   - [Project Constitution](file:///d:/Self_Learning/my-first-project-5-days-google-course/Capstone_Project/docs/project_constitution.md) — Repository values, tech stack, and goals.

2. **Prepare Prerequisites:**
   Ensure you have **Python 3.11+**, **Node.js 18+**, and the fast Python package installer [uv](https://github.com/astral-sh/uv) configured.

3. **Install Dependencies and Pre-commit Hooks:**
   ```bash
   uv sync
   uv run pre-commit install
   ```

4. **Set Up Environments:**
   ```bash
   cp .env.example .env
   # Edit .env with your local credentials and API keys
   ```

---

## 🛡️ Quality and Security Gates

We enforce zero-compromise quality standards before code integrates:
* **Linting & Formatting:** Fast checks powered by `ruff` (automatically configured in `pyproject.toml`).
* **Type-Checking:** Strict `mypy` evaluation to eliminate runtime typing issues.
* **Security Scanning:** Code passes Semgrep checks (configured via [semgrep.yaml](file:///d:/Self_Learning/my-first-project-5-days-google-course/Capstone_Project/.semgrep/semgrep.yaml)) and Yelp's secret detector.
* **Automated Tests:** Execute `uv run pytest` from the root directory to run the test suite.

For detail on branching, PR requirements, and commit rules, refer to [Contribution Guidelines](file:///d:/Self_Learning/my-first-project-5-days-google-course/Capstone_Project/docs/contribution_guidelines.md).

---

## ⚖️ License
Proprietary and Confidential. All rights reserved.
