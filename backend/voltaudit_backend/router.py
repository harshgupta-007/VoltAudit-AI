"""FastAPI router defining REST contracts for invoice audits and manual approvals."""

import uuid
from pathlib import Path

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from voltaudit_backend.config import settings
from voltaudit_backend.schemas import (
    AuditFindingsResponse,
    AuditReportResponse,
    AuditRetryResponse,
    AuditStatusResponse,
    AuditSubmitResponse,
    DiscrepancyInfo,
    HumanOverrideRequest,
    HumanOverrideResponse,
)
from voltaudit_backend.services import AuditService

router = APIRouter(prefix="/audits", tags=["Audits"])


@router.post("/submit", response_model=AuditSubmitResponse)
async def submit_audit(
    invoice_id: str = Form(...), file: UploadFile = File(...)
) -> AuditSubmitResponse:
    """Submit an invoice document path to trigger the multi-agent audit run."""
    # Sanitize and resolve file name to prevent traversal attacks
    safe_filename = Path(file.filename or "invoice.txt").name
    file_path = settings.UPLOAD_DIR / f"{invoice_id}_{safe_filename}"

    try:
        # Write binary content block to uploads directory
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)

        # Run pipeline sequentially via Coordinator
        AuditService.run_audit(invoice_id, str(file_path))
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Audit execution pipeline failed: {exc}"
        ) from exc

    return AuditSubmitResponse(
        invoice_id=invoice_id,
        correlation_id=str(uuid.uuid4()),
        status="COMPLETED",
    )


@router.get("/{invoice_id}/status", response_model=AuditStatusResponse)
def get_audit_status(invoice_id: str) -> AuditStatusResponse:
    """Fetch status, scores, and human verification needs for an invoice run."""
    context = AuditService.get_context(invoice_id)
    if not context:
        raise HTTPException(
            status_code=404, detail=f"Audit execution trace not found: {invoice_id}"
        )

    return AuditStatusResponse(
        invoice_id=invoice_id,
        compliance_score=context.compliance_score,
        risk_classification=context.risk_classification,
        approval_status=context.approval_status,
        human_approval_required=context.human_approval_required,
        override_justification=context.override_justification,
    )


@router.get("/{invoice_id}/report", response_model=AuditReportResponse)
def get_audit_report(invoice_id: str) -> AuditReportResponse:
    """Fetch the explainable markdown run log narrative report."""
    context = AuditService.get_context(invoice_id)
    if not context:
        raise HTTPException(
            status_code=404, detail=f"Audit execution trace not found: {invoice_id}"
        )

    return AuditReportResponse(
        invoice_id=invoice_id,
        report_markdown=context.draft_report or "No report compiled.",
    )


@router.get("/{invoice_id}/findings", response_model=AuditFindingsResponse)
def get_audit_findings(invoice_id: str) -> AuditFindingsResponse:
    """Fetch detailed lists of priced, metered, and historical warning deltas."""
    context = AuditService.get_context(invoice_id)
    if not context:
        raise HTTPException(
            status_code=404, detail=f"Audit execution trace not found: {invoice_id}"
        )

    discrepancies = []
    recon = context.reconciliation_result

    # Compile math variances
    for err in recon.get("math_errors", []):
        discrepancies.append(
            DiscrepancyInfo(
                type="PRICE_MISMATCH", severity="MEDIUM", description=err["description"]
            )
        )

    # Compile physical generation gaps
    if recon.get("quantity_discrepancy"):
        disc = recon["quantity_discrepancy"]
        discrepancies.append(
            DiscrepancyInfo(
                type=disc["type"], severity=disc["severity"], description=disc["description"]
            )
        )

    # Compile historical duplicate checks
    anomaly = context.duplicate_alert
    if anomaly.get("velocity_alert"):
        discrepancies.append(
            DiscrepancyInfo(
                type="DUPLICATE_INVOICE", severity="MEDIUM", description=anomaly["reason"]
            )
        )

    return AuditFindingsResponse(
        invoice_id=invoice_id,
        discrepancies=discrepancies,
        math_errors_count=len(recon.get("math_errors", [])),
    )


@router.post("/{invoice_id}/override", response_model=HumanOverrideResponse)
def apply_manual_override(invoice_id: str, payload: HumanOverrideRequest) -> HumanOverrideResponse:
    """Submit human operator override justifications to approve flagged audits."""
    try:
        success = AuditService.apply_override(invoice_id, payload.justification)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    context = AuditService.get_context(invoice_id)
    approval_status = context.approval_status if context else "PENDING"

    return HumanOverrideResponse(
        invoice_id=invoice_id,
        success=success,
        approval_status=approval_status,
    )


@router.post("/{invoice_id}/retry", response_model=AuditRetryResponse)
def retry_audit_run(invoice_id: str) -> AuditRetryResponse:
    """Re-run the audit pipeline on current cached invoice configurations."""
    try:
        context = AuditService.retry_audit(invoice_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    return AuditRetryResponse(
        invoice_id=invoice_id,
        status="COMPLETED",
        new_compliance_score=context.compliance_score,
    )
