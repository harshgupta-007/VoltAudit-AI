---
name: SPK-001: Document Ingestion Skill Package
description: Ingestion and text node parsing of invoices.
version: 1.0.0
owner: WRK-002
capabilities:
  - CAP-001
---

# SPK-001: Document Ingestion Skill Package

This package manages raw text and coordinate extraction from incoming documents.

## Available Skills

### SPK-001-SK-001: `pdf_character_extractor`
- **Purpose:** Parse text nodes and line bounding coordinates from documents.
- **Inputs:** `file_path: str`
- **Outputs:** `text_blocks: list` of dictionaries representing line-item blocks.

## Usage Example

```python
from spk_001_document_ingestion.scripts.pdf_character_extractor import pdf_character_extractor

result = pdf_character_extractor("/path/to/invoice.pdf")
print(result)
```
