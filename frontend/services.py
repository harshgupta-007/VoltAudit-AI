"""REST client services for calling the VoltAudit FastAPI backend APIs."""

from typing import Any, cast

import requests
from config import settings


class BackendAPIClient:
    """Synchronous REST client for downstream API communications."""

    @staticmethod
    def get_health() -> dict[str, Any]:
        """Fetch backend health and liveness status."""
        try:
            response = requests.get(
                f"{settings.API_BASE_URL.replace('/api/v1', '')}/health", timeout=5
            )
            if response.status_code == 200:
                return cast(dict[str, Any], response.json())
            return {"status": "ERROR", "detail": f"HTTP {response.status_code}"}
        except Exception as exc:
            return {"status": "ERROR", "detail": str(exc)}

    @staticmethod
    def get_ready() -> dict[str, Any]:
        """Fetch backend readiness status."""
        try:
            response = requests.get(
                f"{settings.API_BASE_URL.replace('/api/v1', '')}/ready", timeout=5
            )
            if response.status_code == 200:
                return cast(dict[str, Any], response.json())
            return {"status": "ERROR", "detail": f"HTTP {response.status_code}"}
        except Exception as exc:
            return {"status": "ERROR", "detail": str(exc)}

    @staticmethod
    def submit_audit(invoice_id: str, file_name: str, file_bytes: bytes) -> dict[str, Any]:
        """Upload invoice file stream and initiate audits.

        Args:
            invoice_id: Custom unique code string.
            file_name: Base file name.
            file_bytes: Binary document data.

        Returns:
            JSON response payload.
        """
        try:
            files = {"file": (file_name, file_bytes, "text/plain")}
            data = {"invoice_id": invoice_id}
            response = requests.post(
                f"{settings.API_BASE_URL}/audits/submit",
                data=data,
                files=files,
                timeout=10,
            )
            if response.status_code == 200:
                return cast(dict[str, Any], response.json())
            return {
                "error": f"Submission failed with status {response.status_code}: {response.text}"
            }
        except Exception as exc:
            return {"error": str(exc)}

    @staticmethod
    def get_status(invoice_id: str) -> dict[str, Any]:
        """Fetch audit runs scoring and progression statuses."""
        try:
            response = requests.get(
                f"{settings.API_BASE_URL}/audits/{invoice_id}/status", timeout=5
            )
            if response.status_code == 200:
                return cast(dict[str, Any], response.json())
            return {
                "error": (
                    f"Status lookup failed with status {response.status_code}: {response.text}"
                )
            }
        except Exception as exc:
            return {"error": str(exc)}

    @staticmethod
    def get_report(invoice_id: str) -> dict[str, Any]:
        """Fetch compiled narrative markdown reports."""
        try:
            response = requests.get(
                f"{settings.API_BASE_URL}/audits/{invoice_id}/report", timeout=5
            )
            if response.status_code == 200:
                return cast(dict[str, Any], response.json())
            return {
                "error": (
                    f"Report lookup failed with status {response.status_code}: {response.text}"
                )
            }
        except Exception as exc:
            return {"error": str(exc)}

    @staticmethod
    def get_findings(invoice_id: str) -> dict[str, Any]:
        """Fetch individual parsed discrepancy lists."""
        try:
            response = requests.get(
                f"{settings.API_BASE_URL}/audits/{invoice_id}/findings", timeout=5
            )
            if response.status_code == 200:
                return cast(dict[str, Any], response.json())
            return {
                "error": (
                    f"Findings lookup failed with status {response.status_code}: {response.text}"
                )
            }
        except Exception as exc:
            return {"error": str(exc)}

    @staticmethod
    def apply_override(invoice_id: str, justification: str) -> dict[str, Any]:
        """Submit manual operator override approvals.

        Args:
            invoice_id: Invoice identifier.
            justification: Operator verification comment.

        Returns:
            JSON response payload.
        """
        try:
            response = requests.post(
                f"{settings.API_BASE_URL}/audits/{invoice_id}/override",
                json={"justification": justification},
                timeout=5,
            )
            if response.status_code == 200:
                return cast(dict[str, Any], response.json())
            return {
                "error": (f"Override failed with status {response.status_code}: {response.text}")
            }
        except Exception as exc:
            return {"error": str(exc)}

    @staticmethod
    def retry_audit(invoice_id: str) -> dict[str, Any]:
        """Re-run the audit calculations sequence."""
        try:
            response = requests.post(
                f"{settings.API_BASE_URL}/audits/{invoice_id}/retry", timeout=5
            )
            if response.status_code == 200:
                return cast(dict[str, Any], response.json())
            return {"error": (f"Retry failed with status {response.status_code}: {response.text}")}
        except Exception as exc:
            return {"error": str(exc)}
