"""Audit discrepancy narrative generation."""

import sys
from pathlib import Path
from typing import Any

# Add parent path to load skills_logger
sys.path.append(str(Path(__file__).resolve().parents[2]))
from skills_logger import trace_skill


@trace_skill("SPK-008-SK-001", "narrative_writer")
def narrative_writer(
    compliance_score: int, risk_classification: str, discrepancies: list[dict[str, Any]]
) -> str:
    """Formulate an explainable markdown audit summary citing discrepancy counts and risk levels.

    Args:
        compliance_score: The calculated audit score (0-100).
        risk_classification: Risk tier (LOW, MEDIUM, HIGH).
        discrepancies: Raw discrepancies list.

    Returns:
        Formatted markdown narrative string.
    """
    lines = [
        "## VoltAudit AI Run Report",
        f"- **Compliance Score:** {compliance_score}/100",
        f"- **Audit Risk Classification:** {risk_classification}",
        "",
    ]

    if not discrepancies:
        lines.append("✅ **All validation gates passed. No discrepancies detected.**")
        return "\n".join(lines)

    lines.append("### ⚠️ Identified Audit Findings")
    for idx, error in enumerate(discrepancies, 1):
        err_type = str(error.get("type", "UNKNOWN_ERROR"))
        desc = str(error.get("description", "No description provided."))
        severity = str(error.get("severity", "MEDIUM")).upper()

        lines.append(f"{idx}. **[{severity}] {err_type}**")
        lines.append(f"   - *Explanation:* {desc}")

    return "\n".join(lines)
