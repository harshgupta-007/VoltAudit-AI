# 🌐 VoltAudit AI Application Layer

This directory contains the production-grade **FastAPI Application Layer** for VoltAudit AI, exposing our AI Workforce as secure REST web services.

---

## 1. Architecture Overview

```
                  ┌──────────────────────────────┐
                  │    External REST Clients     │
                  └──────────────┬───────────────┘
                                 │ HTTP (REST)
                  ┌──────────────▼───────────────┐
                  │      FastAPI App Layer       │
                  └──────────────┬───────────────┘
                                 │ invokes execute()
                  ┌──────────────▼───────────────┐
                  │    Coordinator Agent (WRK)   │
                  └──────────────┬───────────────┘
                                 │ orchestrates
                  ┌──────────────▼───────────────┐
                  │    Specialist Workers (WRK)  │
                  └──────────────┬───────────────┘
                    stateless    │        │ reads/writes
                 ┌───────────────┘        └──────────────┐
  ┌──────────────▼──────────────┐         ┌──────────────▼──────────────┐
  │   Antigravity Skills (SPK)  │         │   Model Context Protocol    │
  └─────────────────────────────┘         └─────────────────────────────┘
```

---

## 2. API Contract Guide

### 1. Submit Invoice Audit
* **Method:** `POST`
* **Route:** `/api/v1/audits/submit`
* **Content-Type:** `multipart/form-data`
* **Parameters:**
  - `invoice_id` (Form parameter, string)
  - `file` (Binary file stream upload)
* **Response:**
  ```json
  {
    "invoice_id": "inv-clean-001",
    "correlation_id": "8902ef89-8d99-4d6a-bb90-09abefd90289",
    "status": "COMPLETED"
  }
  ```

### 2. Retrieve Audit Status
* **Method:** `GET`
* **Route:** `/api/v1/audits/{invoice_id}/status`
* **Response:**
  ```json
  {
    "invoice_id": "inv-clean-001",
    "compliance_score": 100,
    "risk_classification": "LOW",
    "approval_status": "APPROVED",
    "human_approval_required": false,
    "override_justification": null
  }
  ```

### 3. Retrieve Findings
* **Method:** `GET`
* **Route:** `/api/v1/audits/{invoice_id}/findings`
* **Response:**
  ```json
  {
    "invoice_id": "inv-clean-001",
    "discrepancies": [],
    "math_errors_count": 0
  }
  ```

### 4. Human Review (Manual Override)
* **Method:** `POST`
* **Route:** `/api/v1/audits/{invoice_id}/override`
* **Body (JSON):**
  ```json
  {
    "justification": "Manual verification of generation logs matches sub-totals."
  }
  ```

### 5. Retry Audit Run
* **Method:** `POST`
* **Route:** `/api/v1/audits/{invoice_id}/retry`

---

## 3. OpenAPI Documentation
Start the dev server:
```bash
uvicorn voltaudit_backend.main:app --reload
```
Navigate to:
- **Interactive docs:** `http://localhost:8000/docs` (Swagger UI)
- **Alternative docs:** `http://localhost:8000/redoc` (ReDoc)
