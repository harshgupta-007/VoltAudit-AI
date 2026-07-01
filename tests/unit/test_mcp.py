"""Unit test suite for the Enterprise MCP Platform."""

import json
import sys
from pathlib import Path

import pytest

# Add mcp/voltaudit_mcp path to sys.path to enable loading
sys.path.append(str(Path(__file__).resolve().parents[2] / "mcp" / "voltaudit_mcp"))

from server import (
    UPLOAD_BASE_DIR,
    create_discrepancy_records,
    lookup_meter_readings,
    notify_human_operator,
    query_active_contracts,
    query_invoice_history,
    query_purchase_orders,
    read_uploaded_file,
    save_audit_run,
    search_canonical_vendors,
)


def test_mcp_read_uploaded_file(tmp_path: Path) -> None:
    """Validate secure file reading and path traversal protections."""
    # Write a test file in the uploads directory
    test_file_id = "test-invoice-101.txt"
    test_file_path = UPLOAD_BASE_DIR / test_file_id
    test_file_path.write_text("Invoice test data blocks.", encoding="utf-8")

    # Verify normal read
    content = read_uploaded_file(test_file_id)
    assert "Invoice test data blocks." in content

    # Clean up test file
    if test_file_path.exists():
        test_file_path.unlink()

    # Verify path traversal protection raises PermissionError
    with pytest.raises(PermissionError):
        read_uploaded_file("../../../pyproject.toml")

    # Verify missing file raises FileNotFoundError
    with pytest.raises(FileNotFoundError):
        read_uploaded_file("nonexistent-file.txt")


def test_mcp_search_canonical_vendors() -> None:
    """Verify vendor fuzzy name searches from SQLite."""
    res_str = search_canonical_vendors("Google")
    res = json.loads(res_str)
    assert len(res) >= 1
    assert res[0]["canonical_name"] == "Google LLC"
    assert res[0]["tax_id"] == "US-1234567"

    # Verify empty lookup returns no results
    empty_res_str = search_canonical_vendors("NonExistentVendor")
    empty_res = json.loads(empty_res_str)
    assert len(empty_res) == 0


def test_mcp_query_active_contracts() -> None:
    """Verify active contract lookup and date validity checking."""
    # Active date range: 2026-06-30 overlaps effective/expiry dates
    res_str = query_active_contracts("vendor-001-google", "2026-06-30")
    res = json.loads(res_str)
    assert len(res) == 1
    assert res[0]["contract_number"] == "CON-GOOGLE-2026"
    assert res[0]["capacity_charge_rate"] == 120.0

    # Date out of range returns empty list
    expired_res_str = query_active_contracts("vendor-001-google", "2027-01-01")
    expired_res = json.loads(expired_res_str)
    assert len(expired_res) == 0


def test_mcp_query_purchase_orders() -> None:
    """Verify purchase order balance queries."""
    res_str = query_purchase_orders("PO-2026-909")
    res = json.loads(res_str)
    assert res["po_number"] == "PO-2026-909"
    assert res["allocated_funds"] == 50000.0

    # Non-existent PO returns empty dictionary
    empty_res_str = query_purchase_orders("PO-NON-EXISTENT")
    empty_res = json.loads(empty_res_str)
    assert not empty_res


def test_mcp_lookup_meter_readings() -> None:
    """Verify physical plant generation meter logs queries."""
    res_str = lookup_meter_readings("MET-WINDFARM-01", "2026-06-01", "2026-07-01")
    res = json.loads(res_str)
    assert len(res) == 1
    assert res[0]["total_generation_mwh"] == 1250.45

    # Out of range date returns empty list
    empty_res_str = lookup_meter_readings("MET-WINDFARM-01", "2026-08-01", "2026-08-31")
    empty_res = json.loads(empty_res_str)
    assert len(empty_res) == 0


def test_mcp_save_audit_run_and_discrepancies() -> None:
    """Verify audit run metrics and discrepancy items inserts."""
    # 1. Save Audit Run
    run_res_str = save_audit_run("invoice-id-test", 85, "WARNINGS")
    run_res = json.loads(run_res_str)
    assert run_res["saved_status"] is True
    audit_run_id = run_res["audit_run_id"]
    assert audit_run_id

    # 2. Save Discrepancy Records
    discrepancies = [
        {
            "type": "PRICE_MISMATCH",
            "severity": "HIGH",
            "description": "Billed rate exceeds contract limit.",
            "expected_value": "100.0",
            "actual_value": "120.0",
        }
    ]
    disc_res_str = create_discrepancy_records(audit_run_id, discrepancies)
    disc_res = json.loads(disc_res_str)
    assert disc_res["discrepancies_created"] == 1


def test_mcp_query_invoice_history() -> None:
    """Verify historical billing records queries."""
    res_str = query_invoice_history("vendor-001-google", "INV-2026-909")
    res = json.loads(res_str)
    assert len(res) == 1
    assert res[0]["total_amount"] == 1080.0


def test_mcp_notify_human_operator() -> None:
    """Verify mock operator email dispatching alert records."""
    res_str = notify_human_operator(
        "operator@voltaudit.com", "invoice-id-test", 45, "High risk audit detected."
    )
    res = json.loads(res_str)
    assert res["alert_dispatched"] is True

    # Assert notification log is written to disk
    notif_file = (
        Path(__file__).resolve().parents[2] / "mcp" / "voltaudit_mcp" / "notifications.json"
    )
    assert notif_file.exists()

    with open(notif_file, encoding="utf-8") as f:
        data = json.load(f)
        assert len(data) >= 1
        assert data[-1]["to"] == "operator@voltaudit.com"
