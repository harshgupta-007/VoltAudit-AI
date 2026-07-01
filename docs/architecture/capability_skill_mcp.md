# 🧩 Capabilities, Skills, and MCP Tools

This document maps business capabilities to stateless agent skills, and details the Model Context Protocol (MCP) server integration boundaries.

---

## 1. Business Capability Architecture

Capabilities represent VoltAudit AI's core business functions rather than technical structures.

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      CORE CAPABILITY: INVOICE AUDITING                  │
└────────────────────────────────────┬────────────────────────────────────┘
                                     │
      ┌────────────────┬─────────────┴───┬─────────────┬──────────────┐
      ▼                ▼                 ▼             ▼              ▼
┌───────────┐    ┌───────────┐    ┌───────────┐  ┌───────────┐  ┌───────────┐
│ Document  │    │ Vendor    │    │ Contract  │  │ Billing   │  │ Complian. │
│ Capture   │    │ Resolut.  │    │ Reconcil. │  │ Accuracy  │  │ Observa.  │
└───────────┘    └───────────┘    └───────────┘  └───────────┘  └───────────┘
```

### Capability Ownership & Relationships
1. **Document Capture:** Responsible for receiving PDF/Image files and producing raw data. Governs the *Ingestion Agent*.
2. **Vendor Resolution:** Maps raw vendor names to canonical Vendor Profiles. Has a dependency relationship with the *Document Capture* capability.
3. **Contract Reconciliation:** Locates POs and rate agreements. Governed by the *Contract Matching Agent*.
4. **Billing Accuracy:** Performs tariff rate validations and calculations. Depends on *Contract Reconciliation*.
5. **Compliance Observability:** Compiles reports and highlights anomalies. Depends on *Billing Accuracy*.

---

## 2. Stateless Agent Skills

Skills are independent, composable, and stateless. They represent the "how-to" math or logic libraries consumed by agents.

| Skill Name | Purpose | Inputs | Outputs | Owning Capability |
| :--- | :--- | :--- | :--- | :--- |
| **`pdf_text_extractor`** | Parses raw character nodes and spatial coordinates from digital PDFs. | `file_path: Path` | `raw_text: str` | Document Capture |
| **`fuzzy_match_vendor`** | Executes string matching (Jaro-Winkler, Levenshtein) to identify vendors. | `raw_name: str` | `match_score: float` | Vendor Resolution |
| **`billing_math_calculator`** | Validates item math: `Quantity * Price == Total` with rounding tolerances. | `items: List[dict]` | `recalculated_total: float` | Billing Accuracy |
| **`unit_converter`** | Translates energy parameters (e.g., kW, MW, MWh) into equivalent contract tariff units. | `val: float, from_unit: str` | `converted_val: float` | Billing Accuracy |
| **`narrative_generator`** | Translates raw error codes into structured explanations. | `discrepancies: List[dict]` | `narrative: str` | Compliance Observability |

---

## 3. Model Context Protocol (MCP) Ecosystem

AI agents **must never** execute direct SQL queries or invoke external APIs directly. All resource and system integrations occur through the Model Context Protocol.

```
┌──────────────┐          ┌────────────────┐          ┌───────────────────┐
│ Agent Layer  ├─────────►│  MCP Tool API  ├─────────►│ Enterprise System │
└──────────────┘          └────────────────┘          └───────────────────┘
```

### Excluded Tools and Categories

#### A. Database MCP Server (`voltaudit-db-mcp`)
* **Business Purpose:** Provide secure, audited access to core database tables.
* **Owned Tools:**
  1. `get_canonical_vendor(vendor_name: str) -> dict`: Resolves a vendor string.
  2. `get_active_contract(vendor_id: str, date: str) -> dict`: Fetches rate sheet.
  3. `get_purchase_order(po_number: str) -> dict`: Fetches PO totals.
  4. `save_audit_run(run_data: dict) -> dict`: Saves an execution run.
  5. `create_discrepancies(discrepancies: list) -> list`: Writes discrepancies.
* **Permissions:** Read-write access to `invoices`, `audit_runs`, and `discrepancies`. Read-only access to `vendors` and `contracts`.
* **Consuming Agents:** Contract Matching Agent, Tariff Validation Agent, Reporting Agent.

#### B. Generation Data MCP Server (`voltaudit-meter-mcp`)
* **Business Purpose:** Fetch actual metered energy generation data from power generation logs (3-way match).
* **Owned Tools:**
  1. `get_generation_readings(meter_id: str, start_date: str, end_date: str) -> dict`: Fetches hourly generation logs.
* **Permissions:** Read-only access to generation databases.
* **Consuming Agents:** Tariff Validation Agent.

#### C. Notification MCP Server (`voltaudit-notify-mcp`)
* **Business Purpose:** Alert human reviewers when a high-risk discrepancy is identified.
* **Owned Tools:**
  1. `send_operator_alert(invoice_id: str, risk_score: int, reason: str) -> bool`: Sends email notifications.
* **Permissions:** Write-only socket connectivity to the SMTP relay.
* **Consuming Agents:** Reporting & Anomaly Agent.
