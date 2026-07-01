# ruff: noqa: E402
"""AI Evaluation Framework assessing agent correctness and workflow metrics."""

import sys
from pathlib import Path

# Configure sys.path for test resolving
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT / "antigravity-skills"))
sys.path.append(str(PROJECT_ROOT / "agents"))

from spk_007_risk_scorer.scripts.discrepancy_weigher import discrepancy_weigher
from voltaudit_agents.adk_platform import (
    AgentContext,
    AgentRegistry,
    InvoiceSpecialist,
    RiskSpecialist,
    WorkflowOrchestrator,
)


def test_agent_reasoning_and_scorecard_correctness() -> None:
    """Evaluate compliance scoring correctness against mock discrepancy records."""
    # Test clean run (no deductions)
    clean_res = discrepancy_weigher([], has_exact_duplicate=False)
    assert clean_res["compliance_score"] == 100
    assert clean_res["risk_classification"] == "LOW"

    # Test medium risk anomalies (price mismatch)
    mismatch_disc = [
        {"type": "PRICE_MISMATCH", "severity": "MEDIUM", "description": "Billed rate mismatch."}
    ]
    dirty_res = discrepancy_weigher(mismatch_disc, has_exact_duplicate=False)
    assert dirty_res["compliance_score"] == 85
    assert dirty_res["risk_classification"] == "MEDIUM"

    # Test high risk anomalies (exact duplicates)
    duplicate_res = discrepancy_weigher([], has_exact_duplicate=True)
    assert duplicate_res["compliance_score"] == 0
    assert duplicate_res["risk_classification"] == "HIGH"


def test_workflow_orchestration_tracing(tmp_path: Path) -> None:
    """Evaluate that the Coordinator executes the pipeline sequentially."""
    invoice_path = tmp_path / "google-clean.txt"
    invoice_path.write_text("Clean invoice content.", encoding="utf-8")

    registry = AgentRegistry()
    from voltaudit_agents.adk_platform import (
        CalculationSpecialist,
        ComplianceSpecialist,
        ContractSpecialist,
        CoordinatorAgent,
        InvoiceSpecialist,
        ReportingSpecialist,
        TariffSpecialist,
    )

    registry.register(CoordinatorAgent())
    registry.register(InvoiceSpecialist())
    registry.register(ContractSpecialist())
    registry.register(TariffSpecialist())
    registry.register(CalculationSpecialist())
    registry.register(ComplianceSpecialist())
    registry.register(RiskSpecialist())
    registry.register(ReportingSpecialist())

    orchestrator = WorkflowOrchestrator(registry)
    context = AgentContext(invoice_id="inv-clean-001", file_path=str(invoice_path))

    orchestrator.execute_audit_pipeline(context)

    # All 8 specialists must be traces in step history logs
    trace_agents = {step["agent_id"] for step in context.step_history}

    expected_agents = {"WRK-002", "WRK-003", "WRK-005", "WRK-006", "WRK-008", "WRK-008_reporter"}
    assert expected_agents.issubset(trace_agents)


def test_latency_telemetry_auditability(tmp_path: Path) -> None:
    """Evaluate that latency and confidence metrics are populated in telemetry steps."""
    invoice_path = tmp_path / "clean.txt"
    invoice_path.write_text("Clean invoice content.", encoding="utf-8")

    agent = InvoiceSpecialist()
    context = AgentContext(invoice_id="inv-tel-test", file_path=str(invoice_path))

    agent.execute(context)

    # Telemetry should be captured
    telemetry_logs = [log for log in context.step_history if log["action"] == "telemetry"]
    assert len(telemetry_logs) == 1
    details = telemetry_logs[0]["details"]
    assert "Latency:" in details
    assert "Confidence: 1.0" in details
