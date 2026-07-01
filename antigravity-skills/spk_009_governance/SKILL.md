---
name: SPK-009: Governance & Communication Skill Package
description: Manages review state gates and operator overrides.
version: 1.0.0
owner: WRK-001
capabilities:
  - CAP-009
---

# SPK-009: Governance & Communication Skill Package

Ensures operator overrides are fully justified with appropriate text blocks.

## Available Skills

### SPK-009-SK-001: `override_validator`
- **Purpose:** Validate manual operator audit override justifications.
- **Inputs:** `override_justification: str`
- **Outputs:** `is_valid: bool` indicating compliance check outcome.
