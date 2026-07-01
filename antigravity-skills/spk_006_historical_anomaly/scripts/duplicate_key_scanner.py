"""Historical duplicate and anomaly detection scans."""

import sys
from pathlib import Path
from typing import Any

# Add parent path to load skills_logger
sys.path.append(str(Path(__file__).resolve().parents[2]))
from skills_logger import trace_skill


@trace_skill("SPK-006-SK-001", "duplicate_key_scanner")
def duplicate_key_scanner(
    invoice_number: str, vendor_id: str, amount: float, historical_records: list[dict[str, Any]]
) -> dict[str, Any]:
    """Scan history listings to identify duplicate submissions or velocity alerts.

    Args:
        invoice_number: Current invoice identifier.
        vendor_id: Canonical Vendor ID.
        amount: Total billed amount.
        historical_records: Historical invoice databases matching vendor_id.

    Returns:
        Alert dictionary if duplicate indicators are matched.
    """
    clean_num = invoice_number.strip().lower()
    clean_vendor = vendor_id.strip().lower()

    for record in historical_records:
        rec_num = str(record.get("invoice_number", "")).strip().lower()
        rec_vendor = str(record.get("vendor_id", "")).strip().lower()
        rec_amount = float(record.get("total_amount", 0.0))

        # Check for exact duplicate match
        if rec_num == clean_num and rec_vendor == clean_vendor:
            return {
                "duplicate_found": True,
                "velocity_alert": False,
                "reason": f"Exact match found for invoice number {invoice_number}.",
                "matching_invoice_id": record.get("invoice_id"),
            }

        # Check for velocity alert: same vendor and amount within recent invoices
        if rec_vendor == clean_vendor and abs(rec_amount - amount) < 0.01:
            return {
                "duplicate_found": False,
                "velocity_alert": True,
                "reason": (
                    f"Warning: Invoice with identical billing amount ({amount}) "
                    f"submitted historically on {record.get('invoice_date')}."
                ),
                "matching_invoice_id": record.get("invoice_id"),
            }

    return {"duplicate_found": False, "velocity_alert": False}
