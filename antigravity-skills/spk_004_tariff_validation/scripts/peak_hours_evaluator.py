"""Peak tariff hour multiplier evaluator."""

import sys
from pathlib import Path

# Add parent path to load skills_logger
sys.path.append(str(Path(__file__).resolve().parents[2]))
from skills_logger import trace_skill


@trace_skill("SPK-004-SK-001", "peak_hours_evaluator")
def peak_hours_evaluator(
    billing_hour: int,
    is_weekend: bool,
    peak_hours: list[int],
    peak_multiplier: float = 1.5,
    offpeak_multiplier: float = 1.0,
) -> float:
    """Evaluate utility peaking multipliers based on the transaction hour and weekday.

    Args:
        billing_hour: Hour of generation (0-23).
        is_weekend: True if the day falls on Saturday or Sunday.
        peak_hours: List of peak hours (e.g. [12, 13, 14, 15, 16, 17, 18]).
        peak_multiplier: Multiplier to apply during peak periods (default 1.5).
        offpeak_multiplier: Multiplier during off-peak periods (default 1.0).

    Returns:
        The calculated tariff multiplier.
    """
    if not (0 <= billing_hour <= 23):
        raise ValueError(f"Billing hour must be within range 0-23: received {billing_hour}")

    # Weekends are generally considered off-peak in commercial tariffs
    if is_weekend:
        return offpeak_multiplier

    if billing_hour in peak_hours:
        return peak_multiplier

    return offpeak_multiplier
