---
name: SPK-008: Audit Reporting Skill Package
description: Formulates markdown explanations and audit reports.
version: 1.0.0
owner: WRK-008
capabilities:
  - CAP-008
---

# SPK-008: Audit Reporting Skill Package

Generates plain-text explainable narratives citing specific contract references.

## Available Skills

### SPK-008-SK-001: `narrative_writer`
- **Purpose:** Translate structured discrepancies lists into markdown text blocks.
- **Inputs:** `score: int`, `discrepancies: list`
- **Outputs:** `narrative: str` plain text explanation.
