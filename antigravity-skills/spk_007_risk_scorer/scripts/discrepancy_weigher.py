"""Compliance risk scoring based on discrepancy severities."""

import sys
from pathlib import Path
from typing import Any

# Add parent path to load skills_logger
sys.path.append(str(Path(__file__).resolve().parents[2]))
from skills_logger import trace_skill


@trace_skill("SPK-007-SK-001", "discrepancy_weigher")
def discrepancy_weigher(
    discrepancies: list[dict[str, Any]], has_exact_duplicate: bool = False
) -> dict[str, Any]:
    """Calculate compliance score and risk tier based on warning lists.

    Args:
        discrepancies: List of discrepancy structures.
        has_exact_duplicate: Boolean indicating exact duplicate.

    Returns:
        Dictionary with score (0-100) and classification (LOW, MEDIUM, HIGH).
    """
    if has_exact_duplicate:
        return {
            "compliance_score": 0,
            "risk_classification": "HIGH",
            "deductions_applied": ["EXACT_DUPLICATE_DEDUCTION_100"],
        }

    score = 100
    deductions: list[str] = []

    for error in discrepancies:
        severity = str(error.get("severity", "LOW")).upper()
        err_type = str(error.get("type", "UNKNOWN")).upper()

        if severity == "HIGH" or err_type == "QUANTITY_MISMATCH":
            score -= 30
            deductions.append(f"{err_type}_DEDUCTION_30")
        elif severity == "MEDIUM" or err_type == "PRICE_MISMATCH":
            score -= 15
            deductions.append(f"{err_type}_DEDUCTION_15")
        else:
            score -= 5
            deductions.append(f"{err_type}_DEDUCTION_5")

    # Enforce lower bound boundary
    score = max(0, score)

    # Classify Risk Tier
    if score >= 90:
        classification = "LOW"
    elif score >= 70:
        classification = "MEDIUM"
    else:
        classification = "HIGH"

    return {
        "compliance_score": score,
        "risk_classification": classification,
        "deductions_applied": deductions,
    }
