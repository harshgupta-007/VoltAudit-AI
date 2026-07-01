"""Unit tests for the Streamlit Frontend API Client service layer."""
# ruff: noqa: E402

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

# Configure sys.path to find frontend scripts
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "frontend"))

from services import BackendAPIClient


@patch("requests.get")
def test_frontend_get_health(mock_get: MagicMock) -> None:
    """Verify that get_health parses successful JSON correctly."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"status": "OK", "mcp_connection": True}
    mock_get.return_value = mock_resp

    res = BackendAPIClient.get_health()
    assert res["status"] == "OK"
    assert res["mcp_connection"] is True


@patch("requests.post")
def test_frontend_submit_audit(mock_post: MagicMock) -> None:
    """Verify that submit_audit transmits multipart files correctly."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"invoice_id": "inv-99", "status": "COMPLETED"}
    mock_post.return_value = mock_resp

    res = BackendAPIClient.submit_audit("inv-99", "test.txt", b"Mock content")
    assert res["invoice_id"] == "inv-99"
    assert res["status"] == "COMPLETED"

    # Inspect mock post call arguments
    args, kwargs = mock_post.call_args
    assert "audits/submit" in args[0]
    assert kwargs["data"] == {"invoice_id": "inv-99"}
    assert "file" in kwargs["files"]


@patch("requests.get")
def test_frontend_get_status(mock_get: MagicMock) -> None:
    """Verify status query parsing and fallback errors handling."""
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    mock_resp.text = "Trace not found"
    mock_get.return_value = mock_resp

    # Should gracefully catch HTTP status failures and return error text details
    res = BackendAPIClient.get_status("inv-missing")
    assert "error" in res
    assert "404" in res["error"]


@patch("requests.post")
def test_frontend_apply_override(mock_post: MagicMock) -> None:
    """Verify override justification submission payloads."""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.json.return_value = {"invoice_id": "inv-1", "success": True}
    mock_post.return_value = mock_resp

    res = BackendAPIClient.apply_override("inv-1", "This justification contains enough characters.")
    assert res["success"] is True

    # Inspect JSON body arguments
    args, kwargs = mock_post.call_args
    assert "audits/inv-1/override" in args[0]
    assert kwargs["json"] == {"justification": "This justification contains enough characters."}
