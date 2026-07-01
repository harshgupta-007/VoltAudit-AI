# ADR-0001: Layered Architecture for Separation of Concerns

## Status
Approved

## Context
VoltAudit AI is a complex system involving document processing, entity resolution, database records, and multi-step agent reasoning loops. If these concerns are mixed, the codebase will quickly become unmaintainable, difficult to test, and vulnerable to security exploits. We need a structural design that decouples LLM prompts, business rules, API routing, database updates, and stateless file parsers.

## Alternatives Considered
1. **Monolithic Backend Application:** All logic (API endpoints, database queries, prompts, parser functions) resides in a single python package.
   - *Why rejected:* Monoliths make it difficult to mock components (e.g. testing parsing without a database, or testing math without calling an LLM) and complicate least-privilege security.
2. **Microservices Architecture:** Deploy the parser, database orchestrator, and agents as separate microservices communicating via REST/gRPC.
   - *Why rejected:* Creates significant operational overhead (multiple docker instances to deploy, network latency, distributed logging complexity) that is unnecessary for our initial scale.

## Decision
Adopt a strict **6-layered architecture** implemented within a single codebase using `uv` workspaces:
1. **Business Layer:** Holds contract requirements, active specifications, and auditing policies (YAML/Spec docs).
2. **Capability Layer:** Declares high-level business functions (e.g. Ingestion, Tariff Auditing).
3. **Agent Layer:** Orchestrates autonomous AI reasoning loops (Gemini LLM prompts and sequencing).
4. **Skill Layer:** Holds stateless, testable helper utility libraries (PDF character extraction, fuzzy text matching).
5. **MCP Tool Layer:** Integrates the Agent Layer with databases and external services via the Model Context Protocol.
6. **Infrastructure Layer:** Exposes the API endpoint routing (FastAPI), database engine (SQLModel), and UI dashboard (React/Vite).

## Consequences
- **Positive:**
  - Clear file ownership and decoupling boundaries.
  - High testability: each layer can be tested or mocked independently (e.g., skill math can be validated using pure python unit tests with zero mock databases).
  - Security isolation: LLM prompt injection risks are contained within the low-trust Agent Layer.
- **Negative:**
  - Requires extra boilerplate setup (individual workspace `pyproject.toml` files, imports crossing workspaces).
  - Developers must be disciplined in adhering to layer constraints (e.g. never importing `backend` structures inside `agents`).
