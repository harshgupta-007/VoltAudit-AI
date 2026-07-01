# 🔌 Enterprise MCP Architecture

This document defines the Enterprise Model Context Protocol (MCP) Architecture for **VoltAudit AI**. It establishes the logical tool domains, security firewalls, interaction flows, and traceability mapping for our agent tool integrations.

---

## 1. MCP Domain Catalog

MCP Domains partition integration capabilities into logical, secure system boundaries.

```
                  ┌──────────────────────────────────────────┐
                  │               Agent Layer                │
                  └────────────────────┬─────────────────────┘
                                       │ MCP JSON Protocols
                                       ▼
  ┌────────────────────────────────────────────────────────────────────────┐
  │                           MCP Integration Layer                        │
  │                                                                        │
  │  ┌───────────────┐ ┌───────────────┐ ┌───────────────┐ ┌────────────┐  │
  │  │ Document Serv.│ │ Vendor Serv.  │ │ Contract Serv.│ │ Meter Serv.│  │
  │  │ (MCP-DOM-001) │ │ (MCP-DOM-002) │ │ (MCP-DOM-003) │ │(MCP-DOM-004)  │
  │  └───────────────┘ └───────────────┘ └───────────────┘ └────────────┘  │
  │  ┌─────────────────────────────────┐ ┌───────────────────────────────┐  │
  │  │   Audit & Discrepancy Serv.     │ │      Notification Serv.       │  │
  │  │         (MCP-DOM-005)           │ │         (MCP-DOM-006)         │  │
  │  └─────────────────────────────────┘ └───────────────────────────────┘  │
  └────────────────────────────────────┬───────────────────────────────────┘
                                       │ SQL/IPC/SMTP Connections
                                       ▼
                  ┌──────────────────────────────────────────┐
                  │            Enterprise Systems            │
                  │       (Database, Meter logs, SMTP)       │
                  └──────────────────────────────────────────┘
```

* **MCP-DOM-001: Document Services Domain:** Exposes sandboxed file reading utilities.
* **MCP-DOM-002: Vendor Services Domain:** Exposes query access to the canonical supplier registry.
* **MCP-DOM-003: Contract & PO Services Domain:** Exposes query access to legal and procurement agreements.
* **MCP-DOM-004: Generation Meter Services Domain:** Exposes read-only queries to generation operations.
* **MCP-DOM-005: Audit & Discrepancy Services Domain:** Exposes write access to audit logs, risk scores, and anomalies.
* **MCP-DOM-006: Notification Services Domain:** Exposes write-only access to corporate alerting lines.

---

## 2. MCP Tool Catalog

### MCP-TOOL-001: `read_uploaded_file`
* **Domain:** MCP-DOM-001 (Document Services).
* **Business Purpose:** Safely read raw text blocks of uploaded invoice documents.
* **Owning Capability:** CAP-001 (Invoice Capture & Parsing).
* **Owning AI Worker:** WRK-002 (Document Ingestion Specialist).
* **Security Classification:** Confidential (Restricted File IO).
* **Required Permissions:** Read-only access to `/backend/data/uploads/` directory.
* **Expected Inputs:**
  ```json
  {
    "file_id": "7d9b9a67-5421-4f32-841d-b6a4a6b228b3"
  }
  ```
* **Expected Outputs:**
  ```json
  {
    "file_content_raw": "OCR text stream..."
  }
  ```
* **Error Handling Expectations:** Returns `FILE_NOT_FOUND` if file ID does not exist; returns `FILE_UNREADABLE` if PDF is corrupted.

### MCP-TOOL-002: `search_canonical_vendors`
* **Domain:** MCP-DOM-002 (Vendor Services).
* **Business Purpose:** Identify and match raw supplier strings to canonical vendor accounts.
* **Owning Capability:** CAP-002 (Vendor Identification & Resolution).
* **Owning AI Worker:** WRK-003 (Vendor Resolution Specialist).
* **Security Classification:** Internal (Master Data Query).
* **Required Permissions:** Read-only access to `vendors` table.
* **Expected Inputs:**
  ```json
  {
    "raw_name_string": "Google LLC"
  }
  ```
* **Expected Outputs:**
  ```json
  {
    "vendors": [
      {
        "vendor_id": "e3e8f9c1-523a-4933-911a-22fa56bc8b32",
        "canonical_name": "Google LLC",
        "tax_id": "US-1234567"
      }
    ]
  }
  ```
* **Error Handling Expectations:** Returns empty list if no matches found; returns `DB_QUERY_FAILURE` on database timeout.

### MCP-TOOL-003: `query_active_contracts`
* **Domain:** MCP-DOM-003 (Contract & PO Services).
* **Business Purpose:** Retrieve active contract rate sheets governing the invoice billing cycle.
* **Owning Capability:** CAP-003 (Contract & Agreement Intelligence).
* **Owning AI Worker:** WRK-004 (Contract & PO Matcher).
* **Security Classification:** Confidential (Rate Sheet parameters).
* **Required Permissions:** Read-only access to `contracts` table.
* **Expected Inputs:**
  ```json
  {
    "vendor_id": "e3e8f9c1-523a-4933-911a-22fa56bc8b32",
    "invoice_date": "2026-06-30"
  }
  ```
* **Expected Outputs:**
  ```json
  {
    "contract_id": "c1f8d9a2-563b-4822-9988-12cba5f27c81",
    "rate_sheet": {
      "capacity_charge_rate": 100.00,
      "variable_charge_rate": 0.05,
      "peak_rate_multiplier": 1.5
    }
  }
  ```
* **Error Handling Expectations:** Returns `CONTRACT_NOT_FOUND` if no active agreement exists for the date.

### MCP-TOOL-004: `query_purchase_orders`
* **Domain:** MCP-DOM-003 (Contract & PO Services).
* **Business Purpose:** Retrieve active purchase order balances for reconciliation.
* **Owning Capability:** CAP-003 (Contract & Agreement Intelligence).
* **Owning AI Worker:** WRK-004 (Contract & PO Matcher).
* **Security Classification:** Confidential (Financial parameters).
* **Required Permissions:** Read-only access to `purchase_orders` table.
* **Expected Inputs:**
  ```json
  {
    "po_number": "PO-2026-909"
  }
  ```
* **Expected Outputs:**
  ```json
  {
    "po_id": "b3e8f9c1-523a-4933-911a-22fa56bc8b32",
    "allocated_funds": 50000.00,
    "consumed_funds": 12000.00
  }
  ```
* **Error Handling Expectations:** Returns `PO_NOT_FOUND` if PO number does not exist.

### MCP-TOOL-005: `lookup_meter_readings`
* **Domain:** MCP-DOM-004 (Generation Meter Services).
* **Business Purpose:** Retrieve physical plant generation meter logs to verify billed quantities (3-way match).
* **Owning Capability:** CAP-005 (Billing Calculation & 3-Way Match).
* **Owning AI Worker:** WRK-006 (Meter Reconciliation Auditor).
* **Security Classification:** Confidential (Operational generation metrics).
* **Required Permissions:** Read-only access to metered readings database views.
* **Expected Inputs:**
  ```json
  {
    "meter_id": "MET-WINDFARM-01",
    "start_date": "2026-06-01",
    "end_date": "2026-06-30"
  }
  ```
* **Expected Outputs:**
  ```json
  {
    "total_metered_generation_mwh": 1250.45,
    "reading_records": 720
  }
  ```
* **Error Handling Expectations:** Returns `METER_DATA_UNAVAILABLE` if records for the period are missing.

### MCP-TOOL-006: `save_audit_run`
* **Domain:** MCP-DOM-005 (Audit & Discrepancy Services).
* **Business Purpose:** Save the calculated compliance risk score and audit run outcome.
* **Owning Capability:** CAP-007 (Risk & Compliance Assessment).
* **Owning AI Worker:** WRK-008 (Risk & Report Compiler).
* **Security Classification:** Confidential (Internal Audit logs).
* **Required Permissions:** Write-only insert permissions to `audit_runs` table.
* **Expected Inputs:**
  ```json
  {
    "invoice_id": "7d9b9a67-5421-4f32-841d-b6a4a6b228b3",
    "compliance_score": 85,
    "outcome": "WARNINGS"
  }
  ```
* **Expected Outputs:**
  ```json
  {
    "audit_run_id": "8c7b8a53-4f99-4d22-bcae-21fa33f2b453",
    "saved_status": true
  }
  ```
* **Error Handling Expectations:** Returns `DB_WRITE_FAILURE` on primary key conflict or validation constraints failure.

### MCP-TOOL-007: `create_discrepancy_records`
* **Domain:** MCP-DOM-005 (Audit & Discrepancy Services).
* **Business Purpose:** Persist identified billing discrepancies in the auditing database.
* **Owning Capability:** CAP-008 (Audit Reporting).
* **Owning AI Worker:** WRK-008 (Risk & Report Compiler).
* **Security Classification:** Confidential (Discrepancy audit trail).
* **Required Permissions:** Write-only insert permissions to `discrepancies` table.
* **Expected Inputs:**
  ```json
  {
    "audit_run_id": "8c7b8a53-4f99-4d22-bcae-21fa33f2b453",
    "discrepancies": [
      {
        "type": "PRICE_MISMATCH",
        "severity": "HIGH",
        "description": "Rate $120 exceeds contract cap $100",
        "expected_value": "100.00",
        "actual_value": "120.00"
      }
    ]
  }
  ```
* **Expected Outputs:**
  ```json
  {
    "discrepancies_created": 1
  }
  ```
* **Error Handling Expectations:** Returns `INVALID_AUDIT_RUN_ID` if reference key does not exist.

### MCP-TOOL-008: `query_invoice_history`
* **Domain:** MCP-DOM-005 (Audit & Discrepancy Services).
* **Business Purpose:** Retrieve vendor billing history logs to identify double-billing attempts.
* **Owning Capability:** CAP-006 (Anomalies & Historical Analysis).
* **Owning AI Worker:** WRK-007 (Historical Anomaly Analyst).
* **Security Classification:** Confidential (Historic billing data).
* **Required Permissions:** Read-only access to `invoices` table.
* **Expected Inputs:**
  ```json
  {
    "vendor_id": "e3e8f9c1-523a-4933-911a-22fa56bc8b32",
    "invoice_number": "INV-2026-909"
  }
  ```
* **Expected Outputs:**
  ```json
  {
    "duplicate_detected": true,
    "matching_records": [
      {
        "invoice_id": "1a2b3c4d-5678-90ab-cdef-1234567890ab",
        "invoice_date": "2026-05-15",
        "total_amount": 1080.00
      }
    ]
  }
  ```
* **Error Handling Expectations:** Returns empty list if no historical matches exist.

### MCP-TOOL-009: `notify_human_operator`
* **Domain:** MCP-DOM-006 (Notification Services).
* **Business Purpose:** Send instant email alerts or system notifications for high-risk audits.
* **Owning Capability:** CAP-009 (Human Review & Governance).
* **Owning AI Worker:** WRK-001 (Executive Audit Coordinator).
* **Security Classification:** Internal (System notifications).
* **Required Permissions:** Write-only socket connectivity to the SMTP relay.
* **Expected Inputs:**
  ```json
  {
    "operator_email": "auditor@voltaudit.com",
    "invoice_id": "7d9b9a67-5421-4f32-841d-b6a4a6b228b3",
    "risk_score": 45,
    "summary": "High Risk: Possible duplicate submission detected."
  }
  ```
* **Expected Outputs:**
  ```json
  {
    "alert_dispatched": true
  }
  ```
* **Error Handling Expectations:** Returns `NOTIFICATION_DISPATCH_FAILED` if mail gateway is down.

---

## 3. MCP Interaction & Security Model

AI workers execute tool queries using JSON-RPC payloads over standard input/output (stdio) channels or local HTTP tunnels.

```
┌──────────────┐          ┌──────────────────────┐          ┌───────────────────┐
│ Agent Worker ├─────────►│ MCP Server Gateway   ├─────────►│ Enterprise System │
└──────────────┘          └──────────┬───────────┘          └───────────────────┘
                             (Tool Execution check &
                              SQL parameter binding)
```

### Security Constraints
1. **Access Authorization:** The MCP Gateway authenticates the worker's digital identifier before permitting tool executions. For example, a request to `lookup_meter_readings` submitted by the Ingestion Specialist is rejected with a `403 FORBIDDEN` error.
2. **Tool-Level Isolation:** MCP servers run in separate processes. A crash or compromise in `voltaudit-meter-mcp` does not affect `voltaudit-db-mcp`.
3. **No Dynamic SQL Evaluation:** All database tools compile queries using parameter binding (via SQLModel). Dynamic string building inside tools is prohibited.
4. **Line-item Sanitization:** Any text parameter returned by an MCP tool is sanitized to remove HTML tags and system parameters, mitigating downstream prompt injection attacks on the LLM.

---

## 4. Master Capability-to-Verification Traceability Matrix

This matrix tracks the integration mapping from capability through MCP to testing verification.

| Cap ID | Workforce ID | Skill Package ID | MCP Domain ID | MCP Tool ID | Future ADK Agent | Future Test ID |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CAP-001** | WRK-002 | SPK-001 | **MCP-DOM-001** | **MCP-TOOL-001** | `IngestAgent` | `test_mcp_read_file` |
| **CAP-002** | WRK-003 | SPK-002 | **MCP-DOM-002** | **MCP-TOOL-002** | `VendorAgent` | `test_mcp_search_vendor` |
| **CAP-003** | WRK-004 | SPK-003 | **MCP-DOM-003** | **MCP-TOOL-003**, **MCP-TOOL-004** | `ContractAgent` | `test_mcp_query_contract` |
| **CAP-004** | WRK-005 | SPK-004 | **MCP-DOM-003** | **MCP-TOOL-003** | `TariffAgent` | `test_mcp_tariff_rates` |
| **CAP-005** | WRK-006 | SPK-005 | **MCP-DOM-004** | **MCP-TOOL-005** | `MeterAgent` | `test_mcp_meter_logs` |
| **CAP-006** | WRK-007 | SPK-006 | **MCP-DOM-005** | **MCP-TOOL-008** | `AnomalyAgent` | `test_mcp_invoice_history` |
| **CAP-007** | WRK-008 | SPK-007 | **MCP-DOM-005** | **MCP-TOOL-006** | `ReportAgent` | `test_mcp_save_audit_run` |
| **CAP-008** | WRK-008 | SPK-008 | **MCP-DOM-005** | **MCP-TOOL-007** | `ReportAgent` | `test_mcp_create_warnings` |
| **CAP-009** | WRK-001 | SPK-009 | **MCP-DOM-006** | **MCP-TOOL-009** | `CoordinatorAgent` | `test_mcp_operator_alert` |

---

## 5. Future Mapping Placeholders

* **Future Antigravity Skills:** Under `/antigravity-skills/` to orchestrate tool invocations.
* **Future MCP Tool Groups:** Implemented inside `/mcp/src/voltaudit_mcp/` using standard MCP Python frameworks.
* **Future ADK Agents:** Configured with prompt instructions and tool declarations under `/agents/src/voltaudit_agents/`.
* **Future Evaluation Suites:** Residing in `/tests/` to run JSON schema and error code validations.
* **Future Security Policies:** Semgrep rules in `.semgrep/semgrep.yaml` and SQLite database connection string boundaries.
* **Future UI Components:** Review views (e.g. Audit logs, warning panels) built under `/frontend/src/components/`.
