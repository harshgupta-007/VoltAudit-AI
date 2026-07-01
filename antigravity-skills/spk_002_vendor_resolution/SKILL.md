---
name: SPK-002: Vendor Resolution Skill Package
description: Matches raw supplier strings to canonical records.
version: 1.0.0
owner: WRK-003
capabilities:
  - CAP-002
---

# SPK-002: Vendor Resolution Skill Package

Fuzzy matching utilities to resolve incoming vendor text strings to canonical master IDs.

## Available Skills

### SPK-002-SK-001: `fuzzy_match_vendor`
- **Purpose:** Perform string metric calculations (Levenshtein distance) on vendor names.
- **Inputs:** `raw_name: str`, `candidate_names: list`
- **Outputs:** `matches: list` of matched profiles with confidence scores.
