# ADR-0003: Human-in-the-Loop Gatekeeper for Audit Approvals and ERP Integrations

## Status
Approved

## Context
VoltAudit AI acts as an auditor for high-value electricity generation invoices. If the system were to automatically approve payments, reject claims, or submit chargebacks directly to vendor portals or ERP databases, any model hallucination, parser rounding error, or incorrect regulatory rule matching could result in direct financial losses, vendor billing disputes, or legal liabilities.

## Alternatives Considered
1. **Fully Automated Auditing:** Automatically approve and post invoices with a high compliance score (>95%), and only flag low-score invoices for human review.
   - *Why rejected:* Even high-confidence runs can contain subtle logical errors or false negatives. In financial auditing, a human must remain legally accountable for payment authorizations.

## Decision
Enforce a strict **Human-in-the-Loop (HITL)** gatekeeper architecture:
1. All AI workforce recommendations (Approvals, Rejections, Warnings, Recalculated totals) are considered advisory-only and are stored in a staging/draft state.
2. The UI dashboard must present clear, explainable discrepancy justifications showing exactly which contract rules were violated.
3. Writing the audit result to external ERP ledgers or triggering payment transactions requires an explicit, authenticated action from a human reviewer (approval or override).

## Consequences
- **Positive:**
  - Complete protection against financial leakage caused by LLM hallucinations or parser errors.
  - Complies with corporate audit governance and regulatory financial requirements (e.g. Sarbanes-Oxley).
  - Enables capturing human correction feedback to continuously retrain and evaluate agent models.
- **Negative:**
  - Slower end-to-end processing throughput compared to a fully automated pipeline.
  - Requires designing and maintaining a comprehensive web frontend console for review actions.
