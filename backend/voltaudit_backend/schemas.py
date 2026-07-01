"""Pydantic schemas for the VoltAudit Backend API endpoints."""

from pydantic import BaseModel, Field


class AuditSubmitResponse(BaseModel):
    """Response payload for invoice audit submission."""

    invoice_id: str = Field(description="Unique ID for the submitted invoice run.")
    correlation_id: str = Field(description="Correlation identifier for tracing.")
    status: str = Field(description="Initial audit run state.")


class AuditStatusResponse(BaseModel):
    """Response payload detailing audit run progress and ratings."""

    invoice_id: str
    compliance_score: int
    risk_classification: str
    approval_status: str
    human_approval_required: bool
    override_justification: str | None = None


class AuditReportResponse(BaseModel):
    """Response payload containing compiled narrative reports."""

    invoice_id: str
    report_markdown: str


class DiscrepancyInfo(BaseModel):
    """Error payload detail for discrepancy findings."""

    type: str
    severity: str
    description: str


class AuditFindingsResponse(BaseModel):
    """Response payload containing specific audit findings."""

    invoice_id: str
    discrepancies: list[DiscrepancyInfo]
    math_errors_count: int


class HumanOverrideRequest(BaseModel):
    """Request payload for manual human operator override approval."""

    justification: str = Field(
        min_length=15, description="Full explanation why override is applied."
    )


class HumanOverrideResponse(BaseModel):
    """Response payload for operator overrides."""

    invoice_id: str
    success: bool
    approval_status: str


class AuditRetryResponse(BaseModel):
    """Response payload for re-running audits."""

    invoice_id: str
    status: str
    new_compliance_score: int


class HealthStatus(BaseModel):
    """System health check payload."""

    status: str
    version: str
    mcp_connection: bool
