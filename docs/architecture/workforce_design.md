# 🤖 AI Workforce Design

VoltAudit AI organizes its agent operations around specialized workers. This document defines the mission, responsibilities, skills, tools, inputs, outputs, and boundaries for each worker.

---

## 👥 Worker Directory & Specialization

To maintain system explainability and security, agents are highly specialized. Multi-purpose agents are prohibited.

```
                  ┌─────────────────────────────────┐
                  │      FastAPI API Boundary       │
                  └────────────────┬────────────────┘
                                   │ Trigger
                                   ▼
                   ┌───────────────────────────────┐
                   │    Agent Orchestrator Loop    │
                   └───────┬───────────────┬───────┘
                           │               │
            ┌──────────────┴───┐       ┌───┴──────────────┐
            │   Ingest Agent   │ ───►  │ Matcher Agent    │
            └──────────────────┘       └──────────────────┘
                     │                          │
            ┌────────┴─────────┐       ┌────────┴─────────┐
            │ Audit Agent      │ ───►  │ Report Agent     │
            └──────────────────┘       └──────────────────┘
```

---

## 📂 Agent Definitions

### 1. Document Parsing Agent (Ingest & OCR)
* **Mission:** Ingest raw invoice image or PDF files and output structured JSON payloads.
* **Responsibilities:**
  - Classify document type (Invoice vs Credit Note vs Utility Bill).
  - Extract header metadata (Invoice Number, Date, Total Billed, Vendor String).
  - Extract tabular data containing line items (Descriptions, Quantities, Unit Prices, Taxes).
* **Owned Capability:** Invoice Understanding.
* **Consumed Skills:** `pdf_text_extractor`, `ocr_table_aligner`.
* **Permitted MCP Tools:** `read_uploaded_file`, `save_parsed_invoice_metadata`.
* **Expected Inputs:** File path of the uploaded document (PDF/PNG/JPEG).
* **Expected Outputs:** Structured Pydantic `InvoicePayload` containing headers and line items.
* **Security Boundary:** Read-only access to the upload folder. No direct database access or network connectivity.
* **Evaluation Considerations:** Token-level precision (F1-score) of extracted numbers and entity name strings.

### 2. Contract & PO Matching Agent
* **Mission:** Resolve vendor identities and locate governing active contracts and purchase orders (POs).
* **Responsibilities:**
  - Standardize raw vendor name strings to canonical vendor profiles.
  - Locate governing contract rate sheets matching the invoice date range.
  - Map invoice line items to Purchase Order (PO) line items.
* **Owned Capability:** Contract Interpretation.
* **Consumed Skills:** `entity_resolution_matcher`, `rate_sheet_lookup_index`.
* **Permitted MCP Tools:** `search_canonical_vendors`, `query_active_contracts`, `query_purchase_orders`.
* **Expected Inputs:** Raw vendor string, invoice date, line item descriptions.
* **Expected Outputs:** Canonical Vendor ID, Contract ID, PO ID, governing rate sheet variables.
* **Security Boundary:** Read-only access to vendor, contract, and PO records. Cannot modify any database structures.
* **Evaluation Considerations:** Precision of entity matching; correct detection of expired contracts or mismatched purchase orders.

### 3. Tariff Validation Agent
* **Mission:** Perform mathematical audits of invoice calculations and energy generation tariffs.
* **Responsibilities:**
  - Recalculate line-item calculations (`Quantity * Unit Price`).
  - Verify billed tariff rates against contract rate sheets (e.g., peak/off-peak, seasonal energy adjustments).
  - Cross-check billed amounts against actual metered generation records (3-way match).
* **Owned Capability:** Billing Validation.
* **Consumed Skills:** `billing_math_calculator`, `energy_unit_converter`.
* **Permitted MCP Tools:** `lookup_meter_readings`, `save_audit_calculation_run`.
* **Expected Inputs:** Structured invoice line items, governing rate sheet details, meter reading history.
* **Expected Outputs:** Recalculated total billed, discrepancy list (price mismatch, quantity mismatch, tax miscalculations).
* **Security Boundary:** Operates in a strict sandboxed environment. No system filesystem or network socket access.
* **Evaluation Considerations:** Mathematical accuracy; false-positive rate on minor price rounding differences.

### 4. Reporting & Anomaly Agent
* **Mission:** Synthesize audit findings, detect double-billing, assign compliance risk scores, and write final review reports.
* **Responsibilities:**
  - Query historic vendor invoices to detect duplicate submissions.
  - Generate clear, human-readable explanations of detected audit discrepancies.
  - Calculate a compliance risk score (0 to 100).
* **Owned Capability:** Audit Reporting & Risk Assessment.
* **Consumed Skills:** `natural_language_explainer`, `audit_scorer`.
* **Permitted MCP Tools:** `query_invoice_history`, `create_discrepancy_records`, `notify_human_operator`.
* **Expected Inputs:** Raw audit discrepancies, historic invoice metadata.
* **Expected Outputs:** Final Audit Report document, risk score, recommended action (Approve vs Reject vs Review).
* **Security Boundary:** Write-only access to discrepancy and audit-run database tables.
* **Evaluation Considerations:** Human utility rating of explanations; recall rate of historic double-billing anomalies.
