"""Services layer interfacing FastAPI routers to the ADK Multi-Agent Platform."""
# ruff: noqa: E402

import sys
from pathlib import Path

# Configure sys.path to resolve the agents package
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "agents"))

from voltaudit_agents.adk_platform import (
    AgentContext,
    AgentRegistry,
    CalculationSpecialist,
    ComplianceSpecialist,
    ContractSpecialist,
    CoordinatorAgent,
    InvoiceSpecialist,
    ReportingSpecialist,
    RiskSpecialist,
    TariffSpecialist,
    WorkflowOrchestrator,
)

# In-memory execution store for session caches
audit_store: dict[str, AgentContext] = {}


def get_orchestrator() -> WorkflowOrchestrator:
    """Initialize agent registry and return workflow orchestrator."""
    registry = AgentRegistry()
    registry.register(CoordinatorAgent())
    registry.register(InvoiceSpecialist())
    registry.register(ContractSpecialist())
    registry.register(TariffSpecialist())
    registry.register(CalculationSpecialist())
    registry.register(ComplianceSpecialist())
    registry.register(RiskSpecialist())
    registry.register(ReportingSpecialist())
    return WorkflowOrchestrator(registry)


class AuditService:
    """Orchestrates API calls into ADK Multi-Agent pipeline executions."""

    @staticmethod
    def run_audit(invoice_id: str, file_path: str) -> AgentContext:
        """Execute the multi-agent pipeline and cache results.

        Args:
            invoice_id: The unique ID.
            file_path: Location of raw mock/pdf invoice file.

        Returns:
            The completed AgentContext object.
        """
        # Create run context
        context = AgentContext(invoice_id=invoice_id, file_path=file_path)

        # Trigger orchestrator sequential execution
        orchestrator = get_orchestrator()
        orchestrator.execute_audit_pipeline(context)

        # Cache completed context
        audit_store[invoice_id] = context
        return context

    @staticmethod
    def get_context(invoice_id: str) -> AgentContext | None:
        """Fetch cached audit context for an invoice.

        Args:
            invoice_id: Unique invoice identifier.

        Returns:
            The cached AgentContext or None.
        """
        return audit_store.get(invoice_id)

    @staticmethod
    def apply_override(invoice_id: str, justification: str) -> bool:
        """Apply human operator manual override justification.

        Args:
            invoice_id: The invoice identifier.
            justification: Explanatory justification text.

        Returns:
            Boolean indicating override success.
        """
        context = audit_store.get(invoice_id)
        if not context:
            raise KeyError(f"Audit run context missing: {invoice_id}")

        orchestrator = get_orchestrator()
        success = orchestrator.apply_human_override(context, justification)
        if success:
            audit_store[invoice_id] = context
        return success

    @staticmethod
    def retry_audit(invoice_id: str) -> AgentContext:
        """Retry audit calculations for a cached context.

        Args:
            invoice_id: The invoice run identifier.

        Returns:
            Re-evaluated AgentContext.
        """
        context = audit_store.get(invoice_id)
        if not context:
            raise KeyError(f"Audit run context missing: {invoice_id}")

        # Reset state parameters
        context.errors = []
        context.step_history = []
        context.compliance_score = 100
        context.risk_classification = "LOW"
        context.approval_status = "PENDING"

        orchestrator = get_orchestrator()
        orchestrator.execute_audit_pipeline(context)

        audit_store[invoice_id] = context
        return context
