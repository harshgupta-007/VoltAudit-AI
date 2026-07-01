---
name: SPK-006: Historical Anomaly Analyzer Skill Package
description: Checks for duplicate transactions and double-billing.
version: 1.0.0
owner: WRK-007
capabilities:
  - CAP-006
---

# SPK-006: Historical Anomaly Analyzer Skill Package

Provides anomaly detection metrics, verifying document duplicate statuses.

## Available Skills

### SPK-006-SK-001: `duplicate_key_scanner`
- **Purpose:** Scan historical submissions to identify double-billing attempts.
- **Inputs:** `invoice_number: str`, `amount: float`, `historical_records: list`
- **Outputs:** `duplicate_alert: dict` if match found.
