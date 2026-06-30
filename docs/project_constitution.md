# 📜 Project Constitution

This document lists the foundational guidelines, technology stack invariants, and core architectural principles of the **VoltAudit AI** project. These rules represent the technical consensus of the core team and must not be altered without a formal RFC (Request for Comments) process.

---

## 👁️ Project Vision

VoltAudit AI is an enterprise-grade AI workforce platform designed to automate invoice auditing. The platform reads complex unstructured invoices, extracts relevant line-item data, resolves entity identities (vendors, business units), matches terms against legal contracts, detects compliance anomalies or double-billing fraud, and raises detailed review recommendations.

We build for:
1. **Explainability:** Audits are accompanied by direct textual references to contract terms or tax codes.
2. **Security:** Corporate financial records are processed securely with sandboxed integrations.
3. **Resilience:** System architecture handles dirty OCR inputs and LLM hallucinatory outputs gracefully.

---

## 🛠️ Unified Technology Stack

All workspace packages must stick to the following technology choices:

| Layer | Technology | Rationale |
| :--- | :--- | :--- |
| **Backend API** | Python 3.11+, FastAPI, SQLModel | Python is standard for AI/data engineering. FastAPI is high-performance, async-native, and auto-generates OpenAPI specs. SQLModel unites SQLAlchemy and Pydantic. |
| **Frontend UI** | TypeScript, React, Vite | Modern frontend structure, fast local development reloading, strict type safety. |
| **Styling** | Vanilla CSS | Provides maximum flexibility and control without build-system overhead or library-specific lock-ins. |
| **Dependency Manager** | `uv` (Python), `npm`/`pnpm` (Node) | Fast, reproducible environments using workspaces and locked packages. |
| **AI Integration** | Gemini Pro API / Vertex AI | Enterprise-grade LLMs with extensive context windows and low latency. |
| **Agent Protocols** | Model Context Protocol (MCP) | Declares modular, reusable data fetching and compliance validation tools for agents to query dynamically. |

---

## 🔒 Security & Architectural Invariants

### 1. Zero-Trust Ingestion
Corporate invoices (PDFs, images) must be treated as untrusted and potentially malicious inputs.
* Never execute compiled binaries or scripts extracted from files.
* Sanitize raw OCR extraction strings before feeding them to database fields or LLM context fields.

### 2. Sandboxed Tool Execution
AI agents operating inside the system must not have raw shell access to the host machine. All external tools (DB readers, compliance API fetchers, mail dispatchers) must be declared explicitly as sandboxed functions or via strict MCP endpoints.

### 3. Separation of Prompts and Data
All LLM prompts must separate instructions from invoice data using standard delimiters (e.g. XML tags `<invoice_data>...</invoice_data>`). This helps defend against prompt injection attacks originating from vendor invoices.

### 4. Lockfiles are Canonical
All package lockfiles (`uv.lock`, `package-lock.json`) must be checked into version control. Developers must not use dynamic dependency ranges (`*`, `^`, `~` without locks) in production.
