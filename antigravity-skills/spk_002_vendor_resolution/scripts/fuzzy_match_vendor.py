"""Vendor name resolution fuzzy matcher."""

import sys
from pathlib import Path
from typing import Any

# Add parent path to load skills_logger
sys.path.append(str(Path(__file__).resolve().parents[2]))
from skills_logger import trace_skill


def levenshtein_ratio(s1: str, s2: str) -> float:
    """Calculate the Levenshtein similarity ratio between two strings.

    Args:
        s1: First string.
        s2: Second string.

    Returns:
        Float between 0.0 (no match) and 1.0 (exact match).
    """
    s1_clean = s1.lower().strip()
    s2_clean = s2.lower().strip()

    if s1_clean == s2_clean:
        return 1.0
    if not s1_clean or not s2_clean:
        return 0.0

    rows = len(s1_clean) + 1
    cols = len(s2_clean) + 1
    distance = [[0 for _ in range(cols)] for _ in range(rows)]

    for i in range(1, rows):
        distance[i][0] = i
    for k in range(1, cols):
        distance[0][k] = k

    for col in range(1, cols):
        for row in range(1, rows):
            if s1_clean[row - 1] == s2_clean[col - 1]:
                cost = 0
            else:
                cost = 2  # standard levenshtein edit cost adjustment
            distance[row][col] = min(
                distance[row - 1][col] + 1,  # Deletion
                distance[row][col - 1] + 1,  # Insertion
                distance[row - 1][col - 1] + cost,  # Substitution
            )

    max_len = len(s1_clean) + len(s2_clean)
    return (max_len - distance[len(s1_clean)][len(s2_clean)]) / max_len


@trace_skill("SPK-002-SK-001", "fuzzy_match_vendor")
def fuzzy_match_vendor(raw_name: str, candidate_names: list[str]) -> list[dict[str, Any]]:
    """Compare a raw vendor name string with a list of canonical names.

    Args:
        raw_name: Unstructured raw vendor string.
        candidate_names: List of approved vendor names.

    Returns:
        Sorted list of candidate name matches with similarity ratios.
    """
    results: list[dict[str, Any]] = []
    for name in candidate_names:
        ratio = levenshtein_ratio(raw_name, name)
        results.append({"name": name, "similarity_score": round(ratio, 4)})

    # Sort matches by highest similarity score descending
    results.sort(key=lambda x: float(x["similarity_score"]), reverse=True)
    return results
