# 🏛️ System Architecture Design

This document describes the layered system design, component interactions, and repository directory ownership rules for **VoltAudit AI**.

---

## 1. Architectural Layers & Boundaries

VoltAudit AI is designed using a decoupled, layered architecture to promote modularity, testability, and security-by-default.

```
┌─────────────────────────────────────────────────────────┐
│                     BUSINESS LAYER                      │
│     (Audit Policies, Contracts, Tariffs, Regulations)    │
└───────────────────────────┬─────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────┐
│                    CAPABILITY LAYER                     │
│    (Ingestion, Entity Resolution, Tariff Audit, etc.)   │
└───────────────────────────┬─────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────┐
│                       AGENT LAYER                       │
│    (Autonomous Specialized Workers: Ingest Agent, etc.)  │
└───────────────────────────┬─────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────┐
│                       SKILL LAYER                       │
│     (Stateless, Composable Tools: PDF Parser, Math)     │
└───────────────────────────┬─────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────┐
│                     MCP TOOL LAYER                      │
│       (Model Context Protocol Servers: DB, Lookups)     │
└───────────────────────────┬─────────────────────────────┘
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  INFRASTRUCTURE LAYER                   │
│     (FastAPI Backend, SQLite/Postgres DB, Gemini SDK)   │
└─────────────────────────────────────────────────────────┘
```

### Layer Responsibility matrix

| Layer | Responsibility | Boundary Rule |
| :--- | :--- | :--- |
| **Business Layer** | Defines contract structures, utility tariff rules (e.g. peaking vs off-peak rates), compliance requirements, and double-billing detection thresholds. | Stateless; configuration-driven. Contains no code. |
| **Capability Layer** | Groups high-level business capabilities (e.g. invoice understanding, regulatory auditing). Acts as the interface between API endpoints and agent groups. | Does not contain direct database queries. Orchestrates underlying agents. |
| **Agent Layer** | Specialized autonomous workers executing domain-specific reasoning loops. Consumes skills and interacts with MCP tools. | Agents have no direct network access or DB access. Must operate strictly via MCP tools. |
| **Skill Layer** | Reusable, stateless helper libraries (e.g., table extraction, unit recalculation) written in clean Python. | Must remain side-effect free. Skills cannot save state or query databases. |
| **MCP Tool Layer** | The exclusive integration boundary. Exposes secure database accessors, external API clients, and regulatory lookups to the Agent Layer. | Directly implements the Model Context Protocol (MCP) server spec. |
| **Infrastructure Layer** | Local database (SQLModel), API gateway (FastAPI), containerization (Docker), and direct model access (Google Gemini API SDK). | Enforces strict network isolation. Only the MCP and API server have network sockets. |

---

## 2. Component Interaction & Workflow

The diagram below represents how elements interact during an audit lifecycle:

```mermaid
sequenceDiagram
    autonumber
    actor Human as Human Reviewer
    participant API as FastAPI Backend
    participant Agent as Agent Orchestrator
    participant LLM as Gemini LLM
    participant MCP as MCP Server
    database DB as SQLModel Database

    Human->>API: Upload Invoice PDF
    API->>DB: Save raw invoice (Status: INGESTED)
    API->>Agent: Trigger Audit Pipeline (invoice_id)

    rect rgb(18, 26, 43)
        note right of Agent: Ingestion & Parsing Phase
        Agent->>MCP: Call extract_text_tool(invoice_pdf)
        MCP->>Agent: Return raw structured JSON text
        Agent->>LLM: Parse line items from raw text
        LLM->>Agent: Return structured line items
        Agent->>MCP: Call save_parsed_invoice_tool(items)
        MCP->>DB: Write line items (Status: PARSED)
    end

    rect rgb(28, 38, 55)
        note right of Agent: Auditing & Calculation Phase
        Agent->>MCP: Call lookup_contract_tool(vendor_name)
        MCP->>DB: Search contracts
        DB-->>MCP: Return active rate sheet
        Agent->>LLM: Perform tariff & rate validation checks
        LLM->>Agent: Flag price mismatch or double-billing
        Agent->>MCP: Call save_discrepancy_tool(findings)
        MCP->>DB: Write discrepancies & risk score
    end

    Agent-->>API: Audit Run Complete (Status: WARNINGS)
    API-->>Human: Render Audit Dashboard with Discrepancies
    Human->>API: Approve Audit Report (Human-in-the-Loop)
    API->>DB: Mark Invoice as AUDITED_APPROVED
```

---

## 3. Repository Directory Ownership

Ownership rules ensure that developers (and AI agents) write files strictly within their architectural boundary:

* `/backend/` -> Owned by the **Infrastructure Layer** (FastAPI, database models, Alembic migrations, environment config).
* `/frontend/` -> Owned by the **Infrastructure Layer** (React Console Dashboard, stylesheets, API hooks).
* `/agents/` -> Owned by the **Agent Layer** (Agent orchestration, prompt templates, reasoning loops).
* `/mcp/` -> Owned by the **MCP Tool Layer** (Model Context Protocol endpoints, database tools, contract lookups, regulatory fetching).
* `/antigravity-skills/` -> Owned by the **Skill Layer** (Stateless custom automation skills, parsers).
* `/specs/` -> Owned by the **Business Layer** (Active requirements, mathematical audit formulas, system schemas).
* `/docs/` -> Owned by the **Business Layer** (Engineering guidelines, standards, and architecture).
