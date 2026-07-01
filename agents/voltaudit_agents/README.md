# 🤖 VoltAudit AI ADK Multi-Agent Platform

This directory contains the production-ready **Enterprise ADK Multi-Agent Platform** for VoltAudit AI, using Google's Agent Development Kit design patterns. It coordinates specialized worker agents during the auditing cycle.

---

## 1. Agent Workforce Hierarchy

The platform defines 8 specialized workers (complying with `ai_workforce.md`):

1. **Executive Audit Coordinator (WRK-001):** Supervise workflows and evaluates compliance score gates.
2. **Document Ingestion Specialist (WRK-002):** Extract line-item arrays from raw invoice document paths.
3. **Vendor & Contract Specialist (WRK-003):** Match suppliers and fetch active contracts.
4. **Tariff Validation Specialist (WRK-005):** Re-compute peaking multipliers.
5. **Billing & 3-Way Match Specialist (WRK-006):** Re-verify billing mathematics and match plant meter records.
6. **Historical Anomaly Specialist (WRK-007):** Check duplicate invoice submissions.
7. **Risk Assessment Specialist (WRK-008):** Weight severities and compute risk scores.
8. **Audit Reporting Specialist (WRK-008_reporter):** Formulate plain-text markdown summaries citing warning logs.

---

## 2. Context Management & Telemetry

* **`AgentContext`:** Holds all intermediate results (raw text, vendor ID, contracts rate sheets, calculated scores, and discrepancy lists).
* **Traceability Logging:** Call `context.log_step(agent_id, action, details)` inside agents to preserve execution lineage for auditing.

---

## 3. Developer & Extension Guide

### Adding a New Agent Specialist
1. **Inherit Base Class:** Subclass `ADKAgent` in `adk_platform.py` and define allowed skills/tools:
   ```python
   class SecurityAuditor(ADKAgent):
       id: str = "WRK-009"
       name: str = "Security Auditor"
       system_instruction: str = "Validate document signature encryption states."
       allowed_skills: List[str] = ["SPK-009-SK-002"]

       def run(self, context: AgentContext) -> None:
           # Execute custom skill validations
           context.log_step(self.id, "check_signature", "Verifying hashes.")
   ```
2. **Register Agent:** Register the new subclass inside `AgentRegistry`.
3. **Orchestrate:** Update the `WorkflowOrchestrator.execute_audit_pipeline` execution flow.
