"""Manual operator audit override validation."""

import sys
from pathlib import Path

# Add parent path to load skills_logger
sys.path.append(str(Path(__file__).resolve().parents[2]))
from skills_logger import trace_skill


@trace_skill("SPK-009-SK-001", "override_validator")
def override_validator(override_justification: str) -> bool:
    """Validate operator audit override justification text blocks.

    Args:
        override_justification: Manual text justification typed by operator.

    Returns:
        Boolean indicating validation success.
    """
    clean_just = override_justification.strip()

    # Justification must be non-empty and have a minimum character length
    if len(clean_just) < 15:
        return False

    # Block lazy/non-descriptive entries
    lowered = clean_just.lower()
    lazy_keywords = ["override", "ok", "test", "passed", "approved", "justification"]
    if any(kw in lowered for kw in lazy_keywords):
        return False

    return True
