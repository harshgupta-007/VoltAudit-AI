"""Document character extraction logic."""

import sys
from pathlib import Path
from typing import Any

# Add parent path to load skills_logger
sys.path.append(str(Path(__file__).resolve().parents[2]))
from skills_logger import trace_skill


@trace_skill("SPK-001-SK-001", "pdf_character_extractor")
def pdf_character_extractor(file_path: str) -> list[dict[str, Any]]:
    """Extract text blocks and layouts from simulated document formats.

    Args:
        file_path: The absolute path of the input file.

    Returns:
        List of dictionaries containing text, bounding box, and block index.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Source file not found at: {file_path}")

    # Standardized extraction response format
    blocks: list[dict[str, Any]] = []

    # If it is a mock json file, read directly
    if path.suffix == ".json":
        import json
        from typing import cast

        with open(path, encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return cast(list[dict[str, Any]], data)
            elif isinstance(data, dict) and "text_blocks" in data:
                return cast(list[dict[str, Any]], data["text_blocks"])

    # For text/PDF file simulations, read line by line
    with open(path, encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()

    for idx, line in enumerate(lines):
        clean_line = line.strip()
        if not clean_line:
            continue
        # Construct layout coordinates mock representation
        blocks.append(
            {
                "text": clean_line,
                "x": 50,
                "y": 100 + (idx * 25),
                "width": len(clean_line) * 8,
                "height": 12,
                "block_index": idx,
            }
        )

    return blocks
