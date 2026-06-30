from typing import Any

from fastapi.testclient import TestClient
from voltaudit_backend.main import app


def test_health_check() -> None:
    """Verifies that the backend health check endpoint returns 200 OK."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_mock_fixture(mock_invoice_payload: dict[str, Any]) -> None:
    """Verifies that the shared test fixture is loaded successfully."""
    assert mock_invoice_payload["invoice_number"] == "INV-2026-001"
    assert len(mock_invoice_payload["line_items"]) == 1
