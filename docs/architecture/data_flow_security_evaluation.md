# 🔐 Data Flow, Security, and Evaluation Architecture

This document defines the lifecycle of invoice auditing data, the zero-trust security boundaries, and the framework for evaluating AI workforce quality.

---

## 1. End-to-End Audit Data Flow

```
   [Invoice PDF]
         │
         ▼
 ┌───────────────┐
 │ API Ingestion │ ──► Status: INGESTED
 └───────┬───────┘
         │
         ▼
 ┌───────────────┐
 │ Document      │ ──► Skill: pdf_text_extractor
 │ Parser Agent  │ ──► MCP: save_parsed_invoice_metadata
 └───────┬───────┘
         │
         ▼
 ┌───────────────┐
 │ Contract      │ ──► MCP: search_canonical_vendors & query_active_contracts
 │ Matcher Agent │
 └───────┬───────┘
         │
         ▼
 ┌───────────────┐
 │ Tariff        │ ──► Skill: billing_math_calculator & energy_unit_converter
 │ Audit Agent   │ ──► MCP: lookup_meter_readings
 └───────┬───────┘
         │
         ▼
 ┌───────────────┐
 │ Reporting     │ ──► Skill: narrative_generator
 │ Agent         │ ──► MCP: save_audit_run & create_discrepancies
 └───────┬───────┘
         │
         ▼
 ┌───────────────┐
 │ Human Review  │ ──► Review Console Dashboard
 └───────┬───────┘
         │ Approved
         ▼
   [ERP Gateway]
```

---

## 2. Security Architecture & Trust Boundaries

VoltAudit AI applies a **zero-trust** security model. Because LLMs process untrusted inputs (vendor invoice descriptions), the agent environment is treated as a sandboxed, low-trust boundary.

```
       UNTRUSTED ENVIRONMENT              │         TRUSTED ENVIRONMENT
                                          │
 ┌─────────────┐       ┌─────────────┐    │    ┌─────────────┐       ┌────────────┐
 │  LLM Model  │ ◄───► │ AI Workers  ├────┼───►│  MCP Server ├──────►│ SQLModel DB│
 └─────────────┘       └─────────────┘    │    └─────────────┘       └────────────┘
                                          │     (Enforces SQL
                                          │      Sanitization)
```

### Trust Boundary Rules
1. **Untrusted Filesystem Access:** Agents cannot write directly to the filesystem or create executable scripts. They may only read the uploaded PDF document specified in their input payload.
2. **Network Isolation:** Only the FastAPI API layer and the MCP Server have network ports. Agents communicate strictly via local IPC or the MCP interface.
3. **Prompt Injection Mitigation:** Invoice line-item strings are wrapped in XML tags (`<invoice_text>...</invoice_text>`) inside prompts. Prompt validation filters verify that no system commands exist in raw strings before LLM evaluation.
4. **Structured Schema Validation:** LLM output is parsed and strictly validated using Pydantic schemas. If output fails schema checks, the run is rejected or retried—preventing malformed data injections.
5. **Least Privilege DB Access:** The database credentials used by the database MCP server prohibit dropping tables or altering schemas.

---

## 3. Evaluation and Quality Observability

To ensure our AI workforce remains accurate and explainable, we track metrics across three distinct gates.

```
                  ┌──────────────────────────────────────────┐
                  │          System Evaluation Gates         │
                  └────────────────────┬─────────────────────┘
                                       │
            ┌──────────────────────────┼──────────────────────────┐
            ▼                          ▼                          ▼
 ┌─────────────────────┐    ┌─────────────────────┐    ┌─────────────────────┐
 │    Skill Testing    │    │   Agent Alignment   │    │   Human Feedback    │
 │ (Unit & Parse Accuracy│  │  (Recall, Math F1)  │    │  (Consol Overrides) │
 └─────────────────────┘    └─────────────────────┘    └─────────────────────┘
```

### Evaluation Metrics Scorecard

| Area | Target Metric | Success Target | Evaluation Method |
| :--- | :--- | :--- | :--- |
| **OCR / Parsing** | Character Error Rate (CER) | `< 1.0%` | Golden test dataset comparison against manual double-keyed invoice data. |
| **Entity Matching** | Vendor Resolution Precision | `> 99.0%` | Verification of Jaro-Winkler thresholds against historical vendor database mappings. |
| **Calculation Accuracy**| Floating Point Math Delta | `0.00` | Automated execution verification of total calculation checks. |
| **Discrepancy Recall** | Anomaly Detection Recall | `> 98.0%` | Synthetic injection testing (inserting dummy duplicates and expired contract rates). |
| **Traceability** | Citation Match Rate | `100.0%` | Verification that every discrepancy cited by the reporting agent matches an active contract section. |
| **System Reliability**| API Rate Limit Failures | `0.0%` | Automatic tracking of exponential backoffs and transient failures. |
