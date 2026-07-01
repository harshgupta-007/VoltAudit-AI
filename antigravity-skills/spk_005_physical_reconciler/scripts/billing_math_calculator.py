"""Billing mathematics and physical meter reconciliation."""

import sys
from pathlib import Path
from typing import Any

# Add parent path to load skills_logger
sys.path.append(str(Path(__file__).resolve().parents[2]))
from skills_logger import trace_skill


@trace_skill("SPK-005-SK-001", "billing_math_calculator")
def billing_math_calculator(
    line_items: list[dict[str, Any]], meter_total: float, tolerance_pct: float = 0.5
) -> dict[str, Any]:
    """Recalculate invoice mathematical totals and match billed energy against plant meter readings.

    Args:
        line_items: List of line items, e.g. [{"rate": 100.0, "quantity": 10.0}]
        meter_total: Total physical generation quantity from meter database.
        tolerance_pct: Acceptable percentage variance (default 0.5%).

    Returns:
        Dictionary containing calculations summary and discrepancy reports.
    """
    calculated_subtotal = 0.0
    total_billed_quantity = 0.0
    math_errors: list[dict[str, Any]] = []

    for idx, item in enumerate(line_items):
        rate = float(item.get("rate", 0.0))
        quantity = float(item.get("quantity", 0.0))
        billed_total = float(item.get("billed_total", 0.0))

        # Re-calculate subtotal
        expected_total = round(rate * quantity, 2)
        total_billed_quantity += quantity
        calculated_subtotal += expected_total

        if abs(expected_total - billed_total) > 0.01:
            math_errors.append(
                {
                    "item_index": idx,
                    "description": (
                        f"Arithmetic mismatch. Expected {expected_total}, billed {billed_total}"
                    ),
                    "expected": expected_total,
                    "billed": billed_total,
                }
            )

    # Reconcile quantity against physical meters
    quantity_discrepancy: dict[str, Any] = {}
    delta = total_billed_quantity - meter_total
    pct_variance = 0.0
    if meter_total > 0.0:
        pct_variance = (delta / meter_total) * 100.0

    if abs(pct_variance) > tolerance_pct:
        quantity_discrepancy = {
            "type": "QUANTITY_MISMATCH",
            "billed_quantity": round(total_billed_quantity, 2),
            "meter_quantity": round(meter_total, 2),
            "variance_percentage": round(pct_variance, 4),
            "description": (
                f"Billed volume {total_billed_quantity} exceeds metered volume "
                f"{meter_total} by {round(pct_variance, 4)}% (tolerance limit: {tolerance_pct}%)"
            ),
        }

    return {
        "calculated_subtotal": round(calculated_subtotal, 2),
        "total_billed_quantity": round(total_billed_quantity, 2),
        "math_errors": math_errors,
        "quantity_discrepancy": quantity_discrepancy,
    }
