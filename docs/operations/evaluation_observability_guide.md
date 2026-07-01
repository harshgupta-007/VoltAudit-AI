# 📊 VoltAudit AI Evaluation & Observability Guide

This guide details the evaluation and monitoring architectures for VoltAudit AI.

---

## 1. AI Evaluation Guide

Our evaluation framework uses a programmatic test suite checking three main areas:

1. **Scoring Correctness:** Verifies that compliance score calculations match predetermined risk tier deductions.
2. **Workforce Sequencing:** Verifies that the Coordinator sequential loop executes all specialists.
3. **Resilience & Fault Recovery:** Simulates flaky database queries and checks that retry loops complete successfully.

### Running Evaluation Tests
```bash
uv run pytest tests/evaluation/
```

---

## 2. Observability Architecture

### 1. Structured Logging
All Antigravity Skill package executions use the `@trace_skill` decorator, outputting structured JSON logs to stdout/stderr:
```json
{
  "timestamp": "2026-07-02 01:49:20,508",
  "level": "INFO",
  "message": {
    "skill_id": "SPK-003-SK-001",
    "skill_name": "contract_date_checker",
    "event": "execution_start",
    "args": ["2026-06-30"],
    "kwargs": {}
  }
}
```

### 2. Distributed Tracing
* **Correlation IDs:** FastAPI injects unique `X-Correlation-ID` headers to trace operations from client upload through agent logic to MCP queries.
* **Trace History:** `AgentContext.step_history` maintains audit logs tracking execution state changes:
  - `agent_id`: Bounded worker identity.
  - `action`: Operations (e.g. `parse_invoice`, `telemetry`, `security_violation`).
  - `details`: Diagnostic logs.
