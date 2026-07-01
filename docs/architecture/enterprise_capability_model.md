# 🧩 Enterprise Capability Model

This document defines the Enterprise Capability Model for **VoltAudit AI**. It establishes the business foundations, terminology, and interaction flows governing our AI workforce development.

---

## 1. Business Capability Catalog

Capabilities represent what VoltAudit AI can perform from a business perspective, remaining completely technology-independent.

### 1. Invoice Capture & Parsing
* **Business Purpose:** Capture unstructured incoming billing documents and convert them into standard structured data records.
* **Responsibilities:** Classify document formats, validate metadata availability, and extract line-item transaction grids.
* **Business Inputs:** Unstructured invoice document streams (PDFs, Images, TIFFs).
* **Business Outputs:** Structured invoice metadata records and line-item schedules.
* **Business Rules:** Document must contain an identifiable vendor name, invoice date, and total amount. Mismatched column headers must be mathematically aligned to standard item schemas.
* **Dependencies:** None.
* **Upstream Capabilities:** None.
* **Downstream Capabilities:** Vendor Identification & Resolution.
* **Expected Consumers:** Accounts Payable, Auditing Teams.
* **Future Extensibility:** Extensible to gas, logistics, and cloud hosting invoice schemas.

### 2. Vendor Identification & Resolution
* **Business Purpose:** Map raw vendor strings to canonical vendor legal entities to enable contract and compliance lookups.
* **Responsibilities:** Perform entity resolution, manage vendor profiles, and record vendor tax registration numbers.
* **Business Inputs:** Raw vendor names extracted from documents.
* **Business Outputs:** Canonical Vendor profile identifiers (Vendor ID) and tax validation statuses.
* **Business Rules:** Vendor must exist in the canonical system; otherwise, trigger a Vendor Onboarding workflow. Strings must match at or above a 95% similarity threshold.
* **Dependencies:** Invoice Capture & Parsing.
* **Upstream Capabilities:** Invoice Capture & Parsing.
* **Downstream Capabilities:** Contract & Agreement Intelligence.
* **Expected Consumers:** Procurement, Compliance Officers.
* **Future Extensibility:** Integration with external Dun & Bradstreet or state business registries.

### 3. Contract & Agreement Intelligence
* **Business Purpose:** Retrieve and interpret governing contractual agreements, pricing rate sheets, and delivery terms.
* **Responsibilities:** Index legal agreements, extract pricing formulas, and locate active rate sheets governing specific billing cycles.
* **Business Inputs:** Canonical Vendor ID, invoice transaction date.
* **Business Outputs:** Governing active Contract rate sheet schema and payment terms parameters.
* **Business Rules:** Contract must be active on the invoice date. Late payment penalties and payment terms (e.g. Net 30) must be resolved.
* **Dependencies:** Vendor Identification & Resolution.
* **Upstream Capabilities:** Vendor Identification & Resolution.
* **Downstream Capabilities:** Tariff & Charge Validation, Billing Calculation & 3-Way Match.
* **Expected Consumers:** Legal, Audit, Contract Managers.
* **Future Extensibility:** Automatically extracts discount clauses from raw unstructured legal contract text via LLMs.

### 4. Tariff & Charge Validation
* **Business Purpose:** Verify that billed tariff items conform to regulatory utility pricing filings and contractual pricing schedules.
* **Responsibilities:** Extract peak/off-peak billing intervals, validate seasonal charge multipliers, and verify capacity fee calculations.
* **Business Inputs:** Structured invoice line items, resolved Contract rate sheet details.
* **Business Outputs:** Tariff compliance validation records (verified vs unverified line charges).
* **Business Rules:** Tariff rates must match contract schedules exactly. Seasonal multiplier rules (e.g. Summer Peak vs Winter Base) must correspond to the invoice billing date.
* **Dependencies:** Contract & Agreement Intelligence.
* **Upstream Capabilities:** Contract & Agreement Intelligence.
* **Downstream Capabilities:** Billing Calculation & 3-Way Match.
* **Expected Consumers:** Energy Procurement Managers, Regulatory Compliance Auditors.
* **Future Extensibility:** Automatic synchronization with public utility commission tariff rate API feeds.

### 5. Billing Calculation & 3-Way Match
* **Business Purpose:** Recalculate invoice totals and reconcile billed energy charges against actual generation or meter logs.
* **Responsibilities:** Perform arithmetic calculations (`Quantity * Price == Total`), compute correct tax amounts, and match quantities against physical generation meter outputs.
* **Business Inputs:** Invoice line items, contractual rates, external generation meter reading logs.
* **Business Outputs:** Recalculated billing logs, quantity variance flags.
* **Business Rules:** Discrepancy flags trigger if billed generation exceeds metered generation by more than 0.5% (tolerance limit). Item mathematical checks must be exact.
* **Dependencies:** Tariff & Charge Validation.
* **Upstream Capabilities:** Tariff & Charge Validation.
* **Downstream Capabilities:** Anomalies & Historical Analysis.
* **Expected Consumers:** Financial Control, Generation Operations.
* **Future Extensibility:** Reconciling dynamic locational marginal pricing (LMP) intervals.

### 6. Anomalies & Historical Analysis
* **Business Purpose:** Protect the business against double-billing, duplicate invoice submissions, and velocity anomalies.
* **Responsibilities:** Scan historical invoice logs, identify identical or shifted invoice numbers, and analyze billing rate variance history for a vendor.
* **Business Inputs:** Current invoice metadata, historical invoice databases.
* **Business Outputs:** Anomaly scan results, duplicate transaction warnings.
* **Business Rules:** Flags are raised if an invoice number matches a historical record, or if the billing total matches a recent run within a 30-day window (velocity check).
* **Dependencies:** Billing Calculation & 3-Way Match.
* **Upstream Capabilities:** Billing Calculation & 3-Way Match.
* **Downstream Capabilities:** Risk & Compliance Assessment.
* **Expected Consumers:** Fraud Detection Teams, Internal Audit.
* **Future Extensibility:** Multi-tenant cross-organizational fraud pooling.

### 7. Risk & Compliance Assessment
* **Business Purpose:** Evaluate audit findings and assign a unified risk-compliance score to guide human reviews.
* **Responsibilities:** Aggregate validation warnings, weigh severity metrics, and assign audit confidence metrics.
* **Business Inputs:** Discrepancies list, anomaly scan logs, vendor compliance history.
* **Business Outputs:** Compliance Score (0 to 100) and Audit Risk classification (Low, Medium, High).
* **Business Rules:** Any price mismatch or duplicate warning instantly drops the compliance score below 50. Minor rounding issues result in scores between 80 and 95.
* **Dependencies:** Anomalies & Historical Analysis.
* **Upstream Capabilities:** Anomalies & Historical Analysis.
* **Downstream Capabilities:** Audit Reporting.
* **Expected Consumers:** CFO, Risk Management, Lead Auditors.
* **Future Extensibility:** Machine learning models predicting human audit override behaviors.

### 8. Audit Reporting
* **Business Purpose:** Formulate a comprehensive, explainable audit record justifying any detected discrepancies.
* **Responsibilities:** Translate mathematical differences into plain text explanations, cite contract sections, and compile audit-ready summary documents.
* **Business Inputs:** Audit risk classification, discrepancies list, contract text references.
* **Business Outputs:** Structured Audit Report PDF / JSON.
* **Business Rules:** Every warning must include a clear explanation, cite a contract clause, and state the financial delta.
* **Dependencies:** Risk & Compliance Assessment.
* **Upstream Capabilities:** Risk & Compliance Assessment.
* **Downstream Capabilities:** Human Review & Governance.
* **Expected Consumers:** Internal Audit, External Regulatory Inspectors.
* **Future Extensibility:** Automatic generation of vendor-facing dispute email drafts.

### 9. Human Review & Governance
* **Business Purpose:** Provide a secure human validation interface to review findings, apply overrides, and finalize audit approvals.
* **Responsibilities:** Render audit findings, capture human override justifications, and record approval logs.
* **Business Inputs:** Audit report data, human operator inputs.
* **Business Outputs:** Final Approved Audit Report, signed approval record.
* **Business Rules:** High-risk audit reports (Score < 80) require dual-auth approval. Every manual override must contain a text justification.
* **Dependencies:** Audit Reporting.
* **Upstream Capabilities:** Audit Reporting.
* **Downstream Capabilities:** ERP Gateway (External Systems).
* **Expected Consumers:** Accounts Payable Supervisors, Financial Directors.
* **Future Extensibility:** Biometric or MFA-authorized audit sign-offs.

---

## 2. Capability Interaction Matrix

The matrix below illustrates the relationships between capabilities during execution.

| Capability | Capture | Vendor Resol. | Contract Intel. | Tariff Valid. | 3-Way Match | Hist. Analys. | Risk Assess. | Reporting | Human Rev. |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Invoice Capture** | — | Sequential | — | — | — | — | — | — | — |
| **Vendor Resol.** | — | — | Sequential | — | — | — | — | — | — |
| **Contract Intel.** | — | — | — | Sequential | Parallel | — | — | — | — |
| **Tariff Valid.** | — | — | — | — | Sequential | — | — | — | — |
| **3-Way Match** | — | — | — | — | — | Sequential | — | — | — |
| **Hist. Analys.** | — | — | — | — | — | — | Sequential | — | — |
| **Risk Assess.** | — | — | — | — | — | — | — | Sequential | — |
| **Audit Reporting** | — | — | — | — | — | — | — | — | Sequential |
| **Human Review** | — | — | — | — | — | — | — | — | — |

---

## 3. End-to-End Business Workflows

### Workflow 1: Standard Invoice Audit
Reconciles incoming generation invoices through automated verification to human sign-off.
1. **Trigger:** A new generation invoice PDF is uploaded to the system.
2. **Ingest & Parse:** Capability *Invoice Capture & Parsing* extracts line item quantities, prices, and vendor headers.
3. **Resolve Vendor:** Capability *Vendor Identification & Resolution* maps the raw vendor name to the canonical Vendor ID.
4. **Identify Contract:** Capability *Contract & Agreement Intelligence* fetches the active contract rate rules matching the invoice date.
5. **Validate Rates:** Capability *Tariff & Charge Validation* verifies the billed tariff categories and pricing multipliers.
6. **Reconcile Units:** Capability *Billing Calculation & 3-Way Match* cross-checks billing math and confirms quantities match external plant meter readings.
7. **History Scan:** Capability *Anomalies & Historical Analysis* verifies that the invoice has not been submitted previously.
8. **Assess & Score:** Capability *Risk & Compliance Assessment* calculates the risk profile and score.
9. **Draft Report:** Capability *Audit Reporting* generates a detailed warning log and draft audit report.
10. **Governance Gate:** Capability *Human Review & Governance* presents the draft to the operator for review and sign-off.

### Workflow 2: Invoice Revalidation
Initiated when a human operator overrides an audit finding or submits updated contracts.
1. **Trigger:** Operator modifies active contract rates or overrides a line item classification.
2. **Recalculation:** Capability *Billing Calculation & 3-Way Match* runs a differential recalculation using the newly defined parameters.
3. **Re-score:** Capability *Risk & Compliance Assessment* updates the risk score based on the override parameters.
4. **Re-publish:** Capability *Audit Reporting* updates the audit log and publishes a new revision of the Audit Report.

---

## 4. Domain Glossary

Consistent domain terminology must be used across all files and future components:

* **Invoice:** A vendor's commercial request for payment containing billed amounts, quantities, and dates.
* **Contract:** A legal rate agreement between the corporation and a generation vendor defining energy rates and billing rules.
* **Tariff:** The pricing scheme applied to energy generation (e.g. flat rate, seasonal peak, off-peak pricing).
* **Vendor:** A power generation partner or utility supplier providing invoice documentation.
* **Plant:** The physical power generation station (e.g., wind farm, solar array) associated with the invoice.
* **Billing Cycle:** The chronological interval covered by the invoice (typically calendar months).
* **Capacity Charge:** A fixed fee paid to a power plant for keeping generation capacity available, regardless of whether energy is generated.
* **Variable Charge:** A generation-dependent fee that scales directly with output.
* **Energy Charge:** The per-unit charge (e.g., $/MWh) applied to active power output.
* **Audit Finding:** A discrete discrepancy or error identified during validation (e.g., price mismatch).
* **Compliance Issue:** A regulatory or administrative error on the invoice (e.g. missing tax registration number).
* **Recommendation:** The automated system action suggested to the human operator (Approve, Review, Reject).

---

## 5. Capability Ownership Matrix

Capabilities are partitioned into logical business domains, which map naturally to future software components:

| Business Domain | Owned Capabilities |
| :--- | :--- |
| **Document Ingestion Domain** | Invoice Capture & Parsing |
| **Relationship Management Domain** | Vendor Identification & Resolution, Contract & Agreement Intelligence |
| **Billing & Calculations Domain** | Tariff & Charge Validation, Billing Calculation & 3-Way Match |
| **Risk & Compliance Domain** | Anomalies & Historical Analysis, Risk & Compliance Assessment |
| **Audit Reporting & Governance Domain** | Audit Reporting, Human Review & Governance |

---

## 6. Future Traceability Matrix

This table maps the conceptual Business Capabilities to the planned technical components of the 6-layer architecture.

| Capability | Future Agent | Future Skills | Future MCP Tools | Future APIs |
| :--- | :---: | :---: | :---: | :---: |
| **Invoice Capture** | Document Parsing Agent | `pdf_text_extractor`, `ocr_table_aligner` | `read_uploaded_file` | `POST /invoices/ingest` |
| **Vendor Resol.** | Contract Matching Agent | `fuzzy_match_vendor` | `search_canonical_vendors` | `POST /vendors/resolve` |
| **Contract Intel.** | Contract Matching Agent | `rate_sheet_lookup_index` | `query_active_contracts` | `GET /contracts/active` |
| **Tariff Valid.** | Tariff Validation Agent | `energy_unit_converter` | `lookup_meter_readings` | `POST /audits/validate` |
| **3-Way Match** | Tariff Validation Agent | `billing_math_calculator` | `lookup_meter_readings` | `POST /audits/calculate` |
| **Hist. Analys.** | Reporting & Anomaly Agent | `fuzzy_match_vendor` | `query_invoice_history` | `GET /invoices/history` |
| **Risk Assess.** | Reporting & Anomaly Agent | `audit_scorer` | `save_audit_run` | `GET /audits/score` |
| **Audit Reporting** | Reporting & Anomaly Agent | `narrative_generator` | `create_discrepancy_records` | `GET /audits/report` |
| **Human Review** | Reporting & Anomaly Agent | `narrative_generator` | `notify_human_operator` | `POST /audits/approve` |
