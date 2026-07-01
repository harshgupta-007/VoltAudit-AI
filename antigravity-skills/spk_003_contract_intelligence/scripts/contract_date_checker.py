"""Contract validity period checker."""

import sys
from datetime import datetime
from pathlib import Path

# Add parent path to load skills_logger
sys.path.append(str(Path(__file__).resolve().parents[2]))
from skills_logger import trace_skill


@trace_skill("SPK-003-SK-001", "contract_date_checker")
def contract_date_checker(invoice_date: str, contract_start: str, contract_end: str) -> bool:
    """Validate if the invoice transaction date lies within the contract period.

    Args:
        invoice_date: The date string (YYYY-MM-DD) from the invoice.
        contract_start: The contract activation date (YYYY-MM-DD).
        contract_end: The contract expiration date (YYYY-MM-DD).

    Returns:
        Boolean indicating validity.
    """
    try:
        inv_dt = datetime.strptime(invoice_date.strip(), "%Y-%m-%d")
        start_dt = datetime.strptime(contract_start.strip(), "%Y-%m-%d")
        end_dt = datetime.strptime(contract_end.strip(), "%Y-%m-%d")
    except ValueError as exc:
        raise ValueError(
            f"Invalid date format provided. Dates must follow YYYY-MM-DD: {exc}"
        ) from exc

    return start_dt <= inv_dt <= end_dt
