---
name: SPK-003: Contract Intelligence Skill Package
description: Validates contract rate sheets and expiry overlays.
version: 1.0.0
owner: WRK-004
capabilities:
  - CAP-003
---

# SPK-003: Contract Intelligence Skill Package

Validates active contracts and parses structural agreement metadata.

## Available Skills

### SPK-003-SK-001: `contract_date_checker`
- **Purpose:** Reconcile billing cycles against contract start and end dates.
- **Inputs:** `invoice_date: str`, `contract_start: str`, `contract_end: str`
- **Outputs:** `is_valid: bool` indicating whether invoice falls within active periods.
