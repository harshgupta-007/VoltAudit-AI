---
name: SPK-005: Physical Reconciler Skill Package
description: Validates billing arithmetic and meter limits.
version: 1.0.0
owner: WRK-006
capabilities:
  - CAP-005
---

# SPK-005: Physical Reconciler Skill Package

Executes invoice line-item arithmetic validation and reconciles quantities with generation logs.

## Available Skills

### SPK-005-SK-001: `billing_math_calculator`
- **Purpose:** Validate item totals and cross-check quantities against plant meter logs.
- **Inputs:** `line_items: list`, `meter_total: float`, `tolerance: float`
- **Outputs:** `reconciliation_result: dict` with discrepancies lists and math verification logs.
