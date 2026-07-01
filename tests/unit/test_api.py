"""Unit test suite for the FastAPI Application Layer APIs."""

from pathlib import Path

from fastapi.testclient import TestClient
from voltaudit_backend.main import app

client = TestClient(app)


def test_system_health_checks() -> None:
    """Verify health, ready, and liveness endpoints return 200 OK."""
    for endpoint in ["/health", "/ready", "/live"]:
        response = client.get(endpoint)
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert data["mcp_connection"] is True


def test_api_submit_clean_audit(tmp_path: Path) -> None:
    """Verify clean invoice submit, status check, and report compile routes."""
    # Create mock clean invoice document
    invoice_path = tmp_path / "google-clean.txt"
    invoice_path.write_text("Mock invoice text.", encoding="utf-8")

    # Post multipart form data
    with open(invoice_path, "rb") as f:
        response = client.post(
            "/api/v1/audits/submit",
            data={"invoice_id": "inv-clean-001"},
            files={"file": ("google-clean.txt", f, "text/plain")},
        )
    assert response.status_code == 200
    data = response.json()
    assert data["invoice_id"] == "inv-clean-001"
    assert data["status"] == "COMPLETED"
    assert "correlation_id" in data

    # Retrieve status check
    status_response = client.get("/api/v1/audits/inv-clean-001/status")
    assert status_response.status_code == 200
    status_data = status_response.json()
    assert status_data["compliance_score"] == 100
    assert status_data["risk_classification"] == "LOW"
    assert status_data["approval_status"] == "APPROVED"
    assert status_data["human_approval_required"] is False

    # Retrieve report check
    report_response = client.get("/api/v1/audits/inv-clean-001/report")
    assert report_response.status_code == 200
    report_data = report_response.json()
    assert "VoltAudit AI Run Report" in report_data["report_markdown"]

    # Retrieve findings check
    findings_response = client.get("/api/v1/audits/inv-clean-001/findings")
    assert findings_response.status_code == 200
    findings_data = findings_response.json()
    assert len(findings_data["discrepancies"]) == 0
    assert findings_data["math_errors_count"] == 0


def test_api_submit_dirty_audit_and_override_gate(tmp_path: Path) -> None:
    """Verify dirty invoice submit, score escalation, and override checkpoints."""
    invoice_path = tmp_path / "google-dirty.txt"
    invoice_path.write_text("Mock dirty text.", encoding="utf-8")

    with open(invoice_path, "rb") as f:
        response = client.post(
            "/api/v1/audits/submit",
            data={"invoice_id": "inv-dirty-001"},
            files={"file": ("google-dirty.txt", f, "text/plain")},
        )
    assert response.status_code == 200

    # Retrieve status check (compliance score should drop to 70)
    status_response = client.get("/api/v1/audits/inv-dirty-001/status")
    assert status_response.status_code == 200
    status_data = status_response.json()
    assert status_data["compliance_score"] == 70
    assert status_data["risk_classification"] == "MEDIUM"
    assert status_data["human_approval_required"] is True
    assert status_data["approval_status"] == "PENDING"

    # Submit invalid human override request (too short justification)
    override_short = client.post(
        "/api/v1/audits/inv-dirty-001/override",
        json={"justification": "ok"},
    )
    # Pydantic v2 min_length=15 validation will fail and return 422 Unprocessable Entity
    assert override_short.status_code == 422

    # Submit valid but lazy justification override request
    override_lazy = client.post(
        "/api/v1/audits/inv-dirty-001/override",
        json={"justification": "This is a short but valid length override statement."},
    )
    # The override_validator checks for specific details;
    # short lazy statement will fail validation rules
    assert override_lazy.status_code == 200

    assert override_lazy.json()["success"] is False
    assert override_lazy.json()["approval_status"] == "PENDING"

    # Submit valid operator override justification
    override_valid = client.post(
        "/api/v1/audits/inv-dirty-001/override",
        json={"justification": "Billed rate is correct per seasonal adjustment data logs."},
    )
    assert override_valid.status_code == 200
    assert override_valid.json()["success"] is True
    assert override_valid.json()["approval_status"] == "APPROVED"


def test_api_submit_nonexistent_invoice_status_checks() -> None:
    """Verify that querying nonexistent invoices returns 404 Not Found."""
    for path in ["status", "report", "findings"]:
        response = client.get(f"/api/v1/audits/non-existent-invoice-id/{path}")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()
