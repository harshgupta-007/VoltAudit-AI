from typing import Any

import pytest


@pytest.fixture
def mock_invoice_payload() -> dict[str, Any]:
    """Returns a standard dummy parsed invoice payload for testing."""
    return {
        "invoice_number": "INV-2026-001",
        "invoice_date": "2026-06-30",
        "raw_vendor_name": "Test Vendor LLC",
        "subtotal": 1000.00,
        "tax_amount": 80.00,
        "total_amount": 1080.00,
        "currency": "USD",
        "line_items": [
            {
                "description": "Consulting Services - Phase 1",
                "quantity": 10,
                "unit_price": 100.00,
                "total_price": 1000.00,
                "tax_rate": 0.08,
            }
        ],
    }


@pytest.fixture(autouse=True)
def mock_env_variables(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensures test runs do not read or require live API keys or active databases."""
    monkeypatch.setenv("ENV", "test")
    monkeypatch.setenv("DATABASE_URL", "sqlite:///:memory:")
    monkeypatch.setenv("GEMINI_API_KEY", "mock_key_for_testing")
