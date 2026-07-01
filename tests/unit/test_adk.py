"""Unit test suite for the Enterprise ADK Multi-Agent Platform."""

import sys
from pathlib import Path

# Add agents path to sys.path to enable loading
sys.path.append(str(Path(__file__).resolve().parents[2] / "agents" / "voltaudit_agents"))

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


def test_adk_agent_registration() -> None:
    """Verify registry saves and discovers agent instances correctly."""
    registry = AgentRegistry()
    coordinator = CoordinatorAgent()
    registry.register(coordinator)

    matched = registry.get_agent("WRK-001")
    assert matched.name == "Executive Audit Coordinator"
    assert (
        "Human Review & Governance" in matched.system_instruction
        or "Human Review" in matched.system_instruction
        or "human approval" in matched.system_instruction
    )


def test_adk_orchestration_passed_run(tmp_path: Path) -> None:
    """Verify end-to-end multi-agent audit run for a clean compliant invoice."""
    # Write a test file simulating invoice uploads
    invoice_path = tmp_path / "google-clean.txt"
    invoice_path.write_text("Clean invoice content.", encoding="utf-8")

    # Initialize Registry and register all 8 workers
    registry = AgentRegistry()
    registry.register(CoordinatorAgent())
    registry.register(InvoiceSpecialist())
    registry.register(ContractSpecialist())
    registry.register(TariffSpecialist())
    registry.register(CalculationSpecialist())
    registry.register(ComplianceSpecialist())
    registry.register(RiskSpecialist())
    registry.register(ReportingSpecialist())

    # Initialize context
    context = AgentContext(invoice_id="inv-clean-001", file_path=str(invoice_path))

    orchestrator = WorkflowOrchestrator(registry)
    orchestrator.execute_audit_pipeline(context)

    # Clean invoice: compliance score should be 100
    assert not context.errors
    assert context.compliance_score == 100
    assert context.risk_classification == "LOW"
    assert context.human_approval_required is False
    assert context.approval_status == "APPROVED"
    assert len(context.step_history) > 5


def test_adk_orchestration_escalation_and_human_override(tmp_path: Path) -> None:
    """Verify that low compliance scores trigger escalation and manual overrides."""
    # Simulating a file upload
    invoice_path = tmp_path / "google-dirty.txt"
    invoice_path.write_text("Dirty invoice content.", encoding="utf-8")

    # Set up mock seed contract database or tweak specialists behavior
    registry = AgentRegistry()
    registry.register(CoordinatorAgent())
    registry.register(InvoiceSpecialist())
    registry.register(ContractSpecialist())
    registry.register(TariffSpecialist())

    # Tweak reconciler to inject quantity mismatch and drop score below 80
    class MismatchReconciler(CalculationSpecialist):
        def run(self, context: AgentContext) -> None:
            # Manually inject error warning delta
            context.reconciliation_result = {
                "math_errors": [],
                "quantity_discrepancy": {
                    "type": "QUANTITY_MISMATCH",
                    "billed_quantity": 2000.0,
                    "meter_quantity": 1000.0,
                    "variance_percentage": 100.0,
                    "description": "Billed volume exceeds metered readings.",
                },
            }
            context.log_step(self.id, "mock_calculation", "Injected quantity mismatch warnings.")

    registry.register(MismatchReconciler())
    registry.register(ComplianceSpecialist())
    registry.register(RiskSpecialist())
    registry.register(ReportingSpecialist())

    context = AgentContext(invoice_id="inv-dirty-001", file_path=str(invoice_path))

    orchestrator = WorkflowOrchestrator(registry)
    orchestrator.execute_audit_pipeline(context)

    # Assert escalation triggered
    assert context.compliance_score == 70  # 100 - 30 (HIGH/QTY)
    assert context.risk_classification == "MEDIUM"
    assert context.human_approval_required is True
    assert context.approval_status == "PENDING"

    # Test applying human override with invalid lazy justification
    lazy_justification = "approved ok"
    success_lazy = orchestrator.apply_human_override(context, lazy_justification)
    assert success_lazy is False
    assert context.approval_status == "PENDING"
    assert context.human_approval_required is True

    # Test applying human override with valid description justification
    valid_justification = "Quantity verified against secondary turbine logs manually."
    success_valid = orchestrator.apply_human_override(context, valid_justification)
    assert success_valid is True
    assert context.approval_status == "APPROVED"
    assert context.human_approval_required is False
    assert context.override_justification == valid_justification
