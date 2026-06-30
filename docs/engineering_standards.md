# 🏛️ Engineering Standards

This document establishes the architectural, resilience, and quality standards for VoltAudit AI. Every engineer (and AI assistant) contributing to this repository must design systems that conform to these specifications.

---

## 🧩 Architectural Principles

### 1. Spec-Driven Development
All features must begin with an approved Specification document (placed in `specs/`) outlining the functional requirements, API payloads, database changes, and user flows before coding commences.

### 2. Modularity & Loose Coupling
- **Separation of Concerns:** Keep the UI (frontend), API router/orchestrator (backend), and AI reasoning tools (agents, MCP) decoupled.
- **Domain Boundaries:** The database models should reflect strict domain structures. Cross-domain queries should go through well-defined service layers, not direct join constructs.
- **Dependency Injection:** Inject external resource clients (database sessions, HTTP clients, LLM providers) rather than hardcoding instantiations within functions.

### 3. Extensibility
Design classes and interfaces using the Open-Closed Principle. For instance, the audit engine should support adding new invoice validation rules by registering a class implementing an `AuditRule` interface without modifying the core auditing orchestrator.

---

## 🛡️ Exception Handling & Fault Tolerance

We aim for zero unhandled exceptions. Apply the following rules:

1. **Domain Exceptions:** Do not raise generic `Exception` or `ValueError`. Define semantic custom exceptions (e.g., `InvoiceParsingError`, `RegulatoryRulesetMissingError`, `TokenLimitExceededError`) deriving from a base `VoltAuditException`.
2. **Boundary Catching:** Catch exceptions at domain boundaries (e.g., API route handlers or consumer entry points) and translate them to standard error responses:
   - For APIs: Return standard JSON error objects with clear diagnostic codes.
   - For Agents: Implement catch-and-retry patterns to handle transient LLM failures.
3. **Graceful Degradation:** If an LLM call fails during auditing, the audit run should status as `FAILED_RETRIABLE` or gracefully log the audit failure without bringing down the entire backend application thread.

---

## 📝 Logging & Observability

We use structured logging to make telemetry parsing straightforward.
* **No `print()` Statements:** Never use standard `print()` or write directly to `sys.stdout`. Use the standard Python `logging` library.
* **Contextual Log Metadata:** Include critical context IDs in logs:
  ```python
  logger.info("Starting audit run for invoice", extra={"invoice_id": invoice.id, "tenant_id": tenant.id})
  ```
* **Log Levels:**
  - `DEBUG`: Fine-grained information for tracing logic.
  - `INFO`: Normal system transactions (e.g., "Audit run completed successfully").
  - `WARNING`: Non-fatal issues (e.g., "API rate limit approaching, sleeping for 2 seconds").
  - `ERROR`: Recoverable runtime faults (e.g., "Failed to load audit rule: RegulatoryComplianceRule").
  - `CRITICAL`: System-wide, unrecoverable crashes (e.g., "Database connection pool exhausted").

---

## 🗄️ Database Operations

- **Expression Builders:** Never concatenate strings to build SQL queries. Use SQLAlchemy or SQLModel query expressions to construct queries dynamically.
- **Scope Sessions Properly:** Use context managers (`async with` or context managers returning `Session`) to ensure database sessions are committed, rolled back on error, and returned to the pool.
- **Migration Policy:** Database schema changes must be declared using migrations (e.g., Alembic). Do not call `metadata.create_all()` in production code.

---

## 🧪 Testing Methodology

We write tests to document system behavior and prevent regressions.

1. **Arrange-Act-Assert (AAA):** Structure all unit tests into clear phases:
   - **Arrange:** Set up mocks, database entries, and variables.
   - **Act:** Execute the function or endpoint being tested.
   - **Assert:** Validate output values, side effects, and mock calls.
2. **Mocking External Services:** Never perform actual API requests to external LLM providers or databases during unit tests. Mock the client responses using tools like `pytest-mock` or custom mock structures.
3. **Coverage Targets:** Target a minimum of **90% coverage** for core business validation logic, audit rules, and api controllers.
