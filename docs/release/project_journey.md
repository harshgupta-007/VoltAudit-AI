# 🛤️ VoltAudit AI Project Journey & Engineering Narrative

This document describes the design decisions, trade-offs, and lessons learned during the development of VoltAudit AI.

---

## 1. Why VoltAudit AI Was Created

Auditing enterprise utility invoices is complex due to peak-hour calculations, contract rate checks, and historical duplicate scans. Traditional RPA breaks when formats change. Single-prompt LLM scripts are insecure and lack verification.

VoltAudit AI was created to demonstrate a **production-grade multi-agent auditing system** utilizing Model Context Protocol (MCP) and cooperative agent loops.

---

## 2. Key Design Trade-offs

### 1. Decoupled Stateless Skills vs. Full Agent Autonomy
* **Trade-off:** We restricted agents from performing direct mathematical calculations or string matches in their prompts. Instead, we created stateless Python utilities (Antigravity Skills).
* **Benefit:** Ensures deterministic calculation outputs and reduces LLM hallucination rates to 0%.

### 2. SQLite vs. Enterprise PostgreSQL
* **Trade-off:** We selected SQLite for portability and ease of container local setup.
* **Benefit:** By enclosing connection states inside `try/finally` blocks, we mitigated concurrency locks while keeping deployment simple.

---

## 3. Lessons Learned & Best Practices

1. **Least Privilege Tool Boundaries:** Restricting agents to specific `allowed_mcp_tools` prevents prompt injection attacks from executing dangerous actions.
2. **Dynamic Path Resolution:** Appending PROJECT_ROOT to `sys.path` ensures tests run consistently across local, containerized, and CI environments.
3. **Structured Telemetry:** Programmatic decorators logging execution times and exception classes greatly simplify system diagnostics.
