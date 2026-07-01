"""Model Context Protocol (MCP) server implementation for VoltAudit AI."""

import json
import logging
import sys
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP

# Ensure local imports work by adding package dir to sys.path
sys.path.append(str(Path(__file__).resolve().parent))
from datetime import UTC

from database import get_connection, init_db

# Setup structured logger
logger = logging.getLogger("voltaudit_mcp")
logger.setLevel(logging.INFO)

# Initialize database schema and seeds
init_db()

mcp = FastMCP("VoltAudit")

# Define Ingestion Base Directory for secure file readings
UPLOAD_BASE_DIR = Path(__file__).resolve().parents[2] / "backend" / "data" / "uploads"
UPLOAD_BASE_DIR.mkdir(parents=True, exist_ok=True)


class FileReadRequest(BaseModel):
    file_id: str = Field(description="The unique name or UUID of the file to read.")


class VendorSearchRequest(BaseModel):
    raw_name_string: str = Field(description="Vendor name search term.")


class ActiveContractsRequest(BaseModel):
    vendor_id: str = Field(description="The canonical Vendor ID.")
    invoice_date: str = Field(description="Invoice billing date (YYYY-MM-DD).")


class PORequest(BaseModel):
    po_number: str = Field(description="The Purchase Order identifier.")


class MeterReadingsRequest(BaseModel):
    meter_id: str = Field(description="Physical generation meter identifier.")
    start_date: str = Field(description="Start boundary date (YYYY-MM-DD).")
    end_date: str = Field(description="End boundary date (YYYY-MM-DD).")


class AuditRunSaveRequest(BaseModel):
    invoice_id: str = Field(description="The invoice ID under audit.")
    compliance_score: int = Field(description="Calculated score (0-100).")
    outcome: str = Field(description="Audit outcome tier (PASSED, WARNINGS, FAILED).")


class DiscrepancyItem(BaseModel):
    type: str = Field(description="Discrepancy category.")
    severity: str = Field(description="Severity (LOW, MEDIUM, HIGH).")
    description: str = Field(description="Detailed error text.")
    expected_value: str | None = Field(None, description="Expected contract parameter.")
    actual_value: str | None = Field(None, description="Actual invoice value.")


class CreateDiscrepanciesRequest(BaseModel):
    audit_run_id: str = Field(description="The reference Audit Run ID.")
    discrepancies: list[DiscrepancyItem] = Field(description="List of detected errors.")


class InvoiceHistoryRequest(BaseModel):
    vendor_id: str = Field(description="The vendor ID.")
    invoice_number: str = Field(description="The invoice identifier.")


class NotificationRequest(BaseModel):
    operator_email: str = Field(description="Operator address.")
    invoice_id: str = Field(description="Invoice ID.")
    risk_score: int = Field(description="Risk scoring metric.")
    summary: str = Field(description="Audit summary text.")


@mcp.tool("MCP-TOOL-001")
def read_uploaded_file(file_id: str) -> str:
    """Read contents of an uploaded invoice file securely."""
    # Sanitize and resolve file path to prevent traversal attacks
    target_path = (UPLOAD_BASE_DIR / file_id).resolve()
    if not target_path.is_relative_to(UPLOAD_BASE_DIR):
        raise PermissionError("Access Denied: Path traversal detected.")

    if not target_path.exists():
        raise FileNotFoundError(f"Requested file does not exist: {file_id}")

    with open(target_path, encoding="utf-8", errors="ignore") as f:
        return f.read()


@mcp.tool("MCP-TOOL-002")
def search_canonical_vendors(raw_name_string: str) -> str:
    """Search for matching canonical vendors in the master database."""
    conn = get_connection()
    cursor = conn.cursor()
    # Enforce safe parameter bindings
    query = "%" + raw_name_string.strip() + "%"
    cursor.execute(
        "SELECT id, canonical_name, tax_id, address FROM vendors WHERE canonical_name LIKE ?;",
        (query,),
    )
    rows = cursor.fetchall()
    conn.close()

    results = [dict(r) for r in rows]
    return json.dumps(results)


@mcp.tool("MCP-TOOL-003")
def query_active_contracts(vendor_id: str, invoice_date: str) -> str:
    """Query contracts table for active agreements matching vendor ID and date."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, vendor_id, contract_number, effective_date, expiry_date,
               payment_terms_days, max_authorized_amount, capacity_charge_rate,
               variable_charge_rate, peak_rate_multiplier
        FROM contracts
        WHERE vendor_id = ? AND ? >= effective_date AND ? <= expiry_date;
        """,
        (vendor_id, invoice_date, invoice_date),
    )
    rows = cursor.fetchall()
    conn.close()

    results = [dict(r) for r in rows]
    return json.dumps(results)


@mcp.tool("MCP-TOOL-004")
def query_purchase_orders(po_number: str) -> str:
    """Query purchase order details matching a PO number."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, po_number, allocated_funds, consumed_funds
        FROM purchase_orders WHERE po_number = ?;
        """,
        (po_number,),
    )
    row = cursor.fetchone()
    conn.close()

    if not row:
        return json.dumps({})
    return json.dumps(dict(row))


@mcp.tool("MCP-TOOL-005")
def lookup_meter_readings(meter_id: str, start_date: str, end_date: str) -> str:
    """Fetch physical plant generation meter logs to verify billed quantities."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, meter_id, reading_date, total_generation_mwh
        FROM meter_readings
        WHERE meter_id = ? AND reading_date >= ? AND reading_date <= ?;
        """,
        (meter_id, start_date, end_date),
    )
    rows = cursor.fetchall()
    conn.close()

    results = [dict(r) for r in rows]
    return json.dumps(results)


@mcp.tool("MCP-TOOL-006")
def save_audit_run(invoice_id: str, compliance_score: int, outcome: str) -> str:
    """Save the final compliance risk score and audit run outcome."""
    import uuid
    from datetime import datetime

    run_id = str(uuid.uuid4())
    executed_at = datetime.now(UTC).isoformat()

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO audit_runs (id, invoice_id, executed_at, compliance_score, outcome)
        VALUES (?, ?, ?, ?, ?);
        """,
        (run_id, invoice_id, executed_at, compliance_score, outcome),
    )
    conn.commit()
    conn.close()

    return json.dumps({"audit_run_id": run_id, "saved_status": True})


@mcp.tool("MCP-TOOL-007")
def create_discrepancy_records(audit_run_id: str, discrepancies: list[dict[str, Any]]) -> str:
    """Persist identified billing discrepancies in the database."""
    import uuid

    conn = get_connection()
    cursor = conn.cursor()
    created_count = 0

    for disc in discrepancies:
        disc_id = str(uuid.uuid4())
        cursor.execute(
            """
            INSERT INTO discrepancies (
                id, audit_run_id, type, severity, description, expected_value, actual_value
            )
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            (
                disc_id,
                audit_run_id,
                disc.get("type"),
                disc.get("severity"),
                disc.get("description"),
                str(disc.get("expected_value", "")),
                str(disc.get("actual_value", "")),
            ),
        )
        created_count += 1

    conn.commit()
    conn.close()

    return json.dumps({"discrepancies_created": created_count})


@mcp.tool("MCP-TOOL-008")
def query_invoice_history(vendor_id: str, invoice_number: str) -> str:
    """Query invoices table to retrieve history logs for double-billing evaluations."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT id, vendor_id, invoice_number, invoice_date, total_amount
        FROM invoices WHERE vendor_id = ? AND invoice_number = ?;
        """,
        (vendor_id, invoice_number),
    )
    rows = cursor.fetchall()
    conn.close()

    results = [dict(r) for r in rows]
    return json.dumps(results)


@mcp.tool("MCP-TOOL-009")
def notify_human_operator(
    operator_email: str, invoice_id: str, risk_score: int, summary: str
) -> str:
    """Simulate dispatching alerts to the human operator gateway."""
    log_msg = {
        "alert_event": "DISPATCH_SMTP_ALERT",
        "to": operator_email,
        "invoice_id": invoice_id,
        "risk_score": risk_score,
        "summary": summary,
    }
    logger.info(json.dumps(log_msg))

    # Append to a local notifications.json log for audit verification
    notif_path = Path(__file__).resolve().parent / "notifications.json"
    try:
        if notif_path.exists():
            with open(notif_path, encoding="utf-8") as rf:
                records = json.load(rf)
        else:
            records = []
    except Exception:
        records = []

    records.append(log_msg)
    with open(notif_path, "w", encoding="utf-8") as wf:
        json.dump(records, wf, indent=2)

    return json.dumps({"alert_dispatched": True})


if __name__ == "__main__":
    mcp.run()
