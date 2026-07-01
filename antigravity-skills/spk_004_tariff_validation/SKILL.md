---
name: SPK-004: Tariff Validation Skill Package
description: Evaluates line-items against peaking multipliers.
version: 1.0.0
owner: WRK-005
capabilities:
  - CAP-004
---

# SPK-004: Tariff Validation Skill Package

Calculates peaking multipliers and validates time-of-use tariffs.

## Available Skills

### SPK-004-SK-001: `peak_hours_evaluator`
- **Purpose:** Determine tariff multipliers based on timestamped transaction intervals.
- **Inputs:** `billing_hour: int`, `is_weekend: bool`, `peak_hours: list`
- **Outputs:** `multiplier: float` tariff adjustment factor.
