---
name: SPK-007: Audit Risk Scorer Skill Package
description: Computes compliance and severity risk scores.
version: 1.0.0
owner: WRK-008
capabilities:
  - CAP-007
---

# SPK-007: Audit Risk Scorer Skill Package

Aggregates warnings and computes structured risk metric scores.

## Available Skills

### SPK-007-SK-001: `discrepancy_weigher`
- **Purpose:** Compute a weighted compliance score (0-100) based on audit discrepancies.
- **Inputs:** `warnings: list`, `has_duplicate: bool`
- **Outputs:** `score: int`, `classification: str`
