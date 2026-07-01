"""Unit test suite for the Enterprise Antigravity Skills Framework."""

import sys
from pathlib import Path

import pytest

# Add antigravity-skills path to sys.path to enable loading
sys.path.append(str(Path(__file__).resolve().parents[2] / "antigravity-skills"))

from spk_001_document_ingestion.scripts.pdf_character_extractor import pdf_character_extractor
from spk_002_vendor_resolution.scripts.fuzzy_match_vendor import fuzzy_match_vendor
from spk_003_contract_intelligence.scripts.contract_date_checker import contract_date_checker
from spk_004_tariff_validation.scripts.peak_hours_evaluator import peak_hours_evaluator
from spk_005_physical_reconciler.scripts.billing_math_calculator import billing_math_calculator
from spk_006_historical_anomaly.scripts.duplicate_key_scanner import duplicate_key_scanner
from spk_007_risk_scorer.scripts.discrepancy_weigher import discrepancy_weigher
from spk_008_audit_reporting.scripts.narrative_writer import narrative_writer
from spk_009_governance.scripts.override_validator import override_validator


def test_spk_001_document_ingestion(tmp_path: Path) -> None:
    """Validate PDF character extractor behavior with text files."""
    test_file = tmp_path / "invoice.txt"
    test_file.write_text("Line 1 text\nLine 2 text\n", encoding="utf-8")

    res = pdf_character_extractor(str(test_file))
    assert len(res) == 2
    assert res[0]["text"] == "Line 1 text"
    assert res[1]["text"] == "Line 2 text"

    # Test file not found error boundary
    with pytest.raises(FileNotFoundError):
        pdf_character_extractor(str(tmp_path / "nonexistent.txt"))


def test_spk_002_vendor_resolution() -> None:
    """Validate Levenshtein similarity fuzzy match scores."""
    candidates = ["Google LLC", "Chevron Corp", "State Utility Corp"]

    # Test exact match
    res1 = fuzzy_match_vendor("Google LLC", candidates)
    assert res1[0]["name"] == "Google LLC"
    assert res1[0]["similarity_score"] == 1.0

    # Test fuzzy match
    res2 = fuzzy_match_vendor("google llc", candidates)
    assert res2[0]["name"] == "Google LLC"
    assert res2[0]["similarity_score"] == 1.0

    # Test fuzzy variations
    res3 = fuzzy_match_vendor("Chevron", candidates)
    assert res3[0]["name"] == "Chevron Corp"
    assert res3[0]["similarity_score"] > 0.5


def test_spk_003_contract_intelligence() -> None:
    """Validate contract date validity period validations."""
    # Test valid overlaps
    assert contract_date_checker("2026-06-15", "2026-01-01", "2026-12-31") is True
    # Test boundary limits
    assert contract_date_checker("2026-01-01", "2026-01-01", "2026-12-31") is True
    # Test out of bounds
    assert contract_date_checker("2025-12-31", "2026-01-01", "2026-12-31") is False

    # Test invalid date formatting failures
    with pytest.raises(ValueError):
        contract_date_checker("invalid-date", "2026-01-01", "2026-12-31")


def test_spk_004_tariff_validation() -> None:
    """Validate peak hours multiplier validations."""
    peak_hours = [12, 13, 14, 15, 16, 17, 18]

    # Test peak hour calculation
    assert peak_hours_evaluator(14, False, peak_hours, 1.5, 1.0) == 1.5
    # Test off-peak hour calculation
    assert peak_hours_evaluator(9, False, peak_hours, 1.5, 1.0) == 1.0
    # Test weekend off-peak override rules
    assert peak_hours_evaluator(14, True, peak_hours, 1.5, 1.0) == 1.0

    # Test hour out of bounds validation
    with pytest.raises(ValueError):
        peak_hours_evaluator(25, False, peak_hours)


def test_spk_005_physical_reconciler() -> None:
    """Validate arithmetic checks and meter reading reconciliations."""
    lines = [
        {"rate": 100.0, "quantity": 10.0, "billed_total": 1000.0},
        {"rate": 50.0, "quantity": 5.0, "billed_total": 250.0},
    ]

    # Test correct calculations matching meter within tolerance limits
    res1 = billing_math_calculator(lines, 15.0, 0.5)
    assert res1["calculated_subtotal"] == 1250.0
    assert len(res1["math_errors"]) == 0
    assert not res1["quantity_discrepancy"]

    # Test math calculation error detection
    bad_lines = [
        {"rate": 100.0, "quantity": 10.0, "billed_total": 950.0}  # math error
    ]
    res2 = billing_math_calculator(bad_lines, 10.0, 0.5)
    assert len(res2["math_errors"]) == 1
    assert res2["math_errors"][0]["expected"] == 1000.0

    # Test meter mismatch delta detection (billed 15, meter 10 -> delta > 0.5%)
    res3 = billing_math_calculator(lines, 10.0, 0.5)
    assert res3["quantity_discrepancy"]["type"] == "QUANTITY_MISMATCH"


def test_spk_006_historical_anomaly() -> None:
    """Validate historical duplicate checks and velocity anomaly alerts."""
    history = [
        {
            "invoice_id": "1",
            "invoice_number": "INV-100",
            "vendor_id": "V-01",
            "total_amount": 1000.0,
            "invoice_date": "2026-05-01",
        }
    ]

    # Test exact duplicate match
    res1 = duplicate_key_scanner("INV-100", "V-01", 1000.0, history)
    assert res1["duplicate_found"] is True

    # Test velocity mismatch warning
    res2 = duplicate_key_scanner("INV-200", "V-01", 1000.0, history)
    assert res2["duplicate_found"] is False
    assert res2["velocity_alert"] is True

    # Test non-matching clean scan
    res3 = duplicate_key_scanner("INV-300", "V-02", 500.0, history)
    assert res3["duplicate_found"] is False
    assert res3["velocity_alert"] is False


def test_spk_007_risk_scorer() -> None:
    """Validate compliance risk scores and classifications."""
    # Test perfect pass
    res1 = discrepancy_weigher([])
    assert res1["compliance_score"] == 100
    assert res1["risk_classification"] == "LOW"

    # Test exact duplicate override
    res2 = discrepancy_weigher([], has_exact_duplicate=True)
    assert res2["compliance_score"] == 0
    assert res2["risk_classification"] == "HIGH"

    # Test severity deductions
    warnings = [
        {"type": "QUANTITY_MISMATCH", "severity": "HIGH"},
        {"type": "PRICE_MISMATCH", "severity": "MEDIUM"},
    ]
    res3 = discrepancy_weigher(warnings)
    # 100 - 30 (HIGH/QTY) - 15 (MEDIUM/PRICE) = 55
    assert res3["compliance_score"] == 55
    assert res3["risk_classification"] == "HIGH"


def test_spk_008_audit_reporting() -> None:
    """Validate compiled report format strings."""
    warnings = [
        {
            "type": "PRICE_MISMATCH",
            "severity": "HIGH",
            "description": "Billed rate exceeds contract limit.",
        }
    ]
    report = narrative_writer(70, "MEDIUM", warnings)
    assert "VoltAudit AI Run Report" in report
    assert "70/100" in report
    assert "PRICE_MISMATCH" in report


def test_spk_009_governance() -> None:
    """Validate human override text checks."""
    # Test valid description
    assert override_validator("Meter read verified manually by Plant Ops.") is True
    # Test short description
    assert override_validator("OK") is False
    # Test lazy descriptor keyword block
    assert override_validator("override approved") is False
