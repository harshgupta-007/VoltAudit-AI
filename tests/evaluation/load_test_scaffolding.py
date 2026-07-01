"""Load testing scaffolding to simulate concurrent audit execution runs."""

import concurrent.futures
import time
from pathlib import Path
from typing import Any

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


def init_orchestrator() -> WorkflowOrchestrator:
    """Helper to initialize the full orchestrator."""
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


def run_single_audit(invoice_id: str, file_path: str) -> dict[str, Any]:
    """Run a single audit pipeline and return performance metrics."""
    orchestrator = init_orchestrator()
    context = AgentContext(invoice_id=invoice_id, file_path=file_path)

    start_time = time.time()
    try:
        orchestrator.execute_audit_pipeline(context)
        success = True
        err_msg = ""
    except Exception as exc:
        success = False
        err_msg = str(exc)
    duration = time.time() - start_time

    return {
        "invoice_id": invoice_id,
        "success": success,
        "duration": duration,
        "error": err_msg,
        "score": context.compliance_score,
    }


def simulate_load(concurrency: int = 5, total_runs: int = 10) -> None:
    """Simulate concurrent audit run load.

    Args:
        concurrency: Number of parallel workers.
        total_runs: Total number of audits to submit.
    """
    print(f"Starting load test simulation (Concurrency: {concurrency}, Total Runs: {total_runs})")

    # Create dummy clean invoice file for testing
    dummy_file = Path("dummy_load_invoice.txt")
    dummy_file.write_text("Mock clean invoice document text.", encoding="utf-8")

    results = []
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=concurrency) as executor:
        futures = {
            executor.submit(run_single_audit, f"load-inv-{i}", str(dummy_file)): i
            for i in range(total_runs)
        }

        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            results.append(res)

    total_duration = time.time() - start_time

    # Cleanup
    if dummy_file.exists():
        dummy_file.unlink()

    # Calculate statistics
    success_count = sum(1 for r in results if r["success"])
    failures = [r for r in results if not r["success"]]
    durations = [r["duration"] for r in results]
    avg_latency = sum(durations) / len(durations) if durations else 0

    print("--- Load Test Results ---")
    print(f"Successful Runs: {success_count}/{total_runs}")
    print(f"Failed Runs: {len(failures)}")
    print(f"Total Time Taken: {total_duration:.4f} seconds")
    print(f"Average Latency: {avg_latency:.4f} seconds")
    print(f"Throughput: {total_runs / total_duration:.2f} runs/sec")

    if failures:
        print(f"First failure error detail: {failures[0]['error']}")


if __name__ == "__main__":
    simulate_load()
