# ruff: noqa: E402
"""Security hardening tests validating Zero-Trust defenses and error sanitization."""

import sys
from pathlib import Path

import pytest

# Configure sys.path for test resolving
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "mcp"))
sys.path.append(str(PROJECT_ROOT / "agents"))

from voltaudit_mcp.server import read_uploaded_file


def test_path_traversal_guards() -> None:
    """Verify that path traversal attempts raise standard FileNotFoundError or PermissionError."""
    # Attempting to load files outside upload boundaries
    for traversal_path in [
        "../database.py",
        "..\\..\\pyproject.toml",
        "/etc/passwd",
        "C:\\Windows\\system32\\cmd.exe",
    ]:
        with pytest.raises((ValueError, FileNotFoundError, PermissionError)):
            read_uploaded_file(traversal_path)


def test_no_hardcoded_secrets_in_environment() -> None:
    """Verify database configurations and files do not expose static credentials."""
    db_file = Path(__file__).resolve().parents[2] / "mcp" / "voltaudit_mcp" / "database.py"
    db_content = db_file.read_text(encoding="utf-8")

    # DB connection should not have hardcoded tokens, users or passwords
    assert "password=" not in db_content.lower()
    assert "token=" not in db_content.lower()
    assert "secret=" not in db_content.lower()


def test_error_message_sanitization() -> None:
    """Verify that raised exception payloads do not leak system path information."""
    from voltaudit_agents.adk_platform import AgentContext, InvoiceSpecialist

    agent = InvoiceSpecialist()
    context = AgentContext(invoice_id="inv-err-test", file_path="nonexistent_folder/invoice.txt")

    with pytest.raises(FileNotFoundError):
        agent.execute(context)

    # Ingestion failure should log an error, but error message
    # should be clean and not leak local OS paths
    assert len(context.errors) > 0
    err_msg = context.errors[0]["error"]
    assert "C:\\" not in err_msg
    assert "Users\\" not in err_msg
    assert "d:\\" not in err_msg
