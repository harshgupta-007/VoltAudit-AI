# 📊 VoltAudit AI Enterprise Streamlit Frontend

This folder houses the **Enterprise Streamlit Frontend** for VoltAudit AI, acting as a thin presentation layer that communicates exclusively with our FastAPI Application Layer.

---

## 1. Frontend Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                    Streamlit Dashboard UI                     │
├───────────────────────────────────────────────────────────────┤
│ [📊 Home]    [📤 Ingest & Audit]    [✍️ Review]    [⚙️ Health] │
└──────────────────────────────┬────────────────────────────────┘
                               │ HTTP REST Requests
┌──────────────────────────────▼────────────────────────────────┐
│                   BackendAPIClient Service                    │
├───────────────────────────────────────────────────────────────┤
│ requests.get() / requests.post()                              │
└──────────────────────────────┬────────────────────────────────┘
                               │ REST Call (JSON/Multipart)
┌──────────────────────────────▼────────────────────────────────┐
│                 FastAPI Backend application                   │
└───────────────────────────────────────────────────────────────┘
```

The frontend uses custom CSS to style Streamlit's native components, rendering custom-branded cards, Outfit/Inter typography, real-time progress steps for active AI workers, and status dials.

---

## 2. Page & Component Guide

1. **Dashboard Home:**
   - Exposes high-level metrics cards (Total Audited, Auto-Approved, Pending Reviews, Average Compliance Score).
   - Draws interactive line charts representing historic audit runs.
2. **Ingest & Audit:**
   - Drag-and-drop area for invoice document uploads.
   - Triggers the `CoordinatorAgent` workflow backend.
   - Animates the live state progression logs of the active specialists.
   - Renders compiled markdown narrative reports and individual discrepancy warnings.
3. **Human Review Queue:**
   - Filters pending audits (compliance score < 80).
   - Allows typing operator overrides.
   - Intercepts and flags lazy keywords or too short entries.
4. **System Health:**
   - Diagnostic dashboard querying liveness and readiness API endpoints.

---

## 3. Operations & Startup

To launch the Streamlit frontend:
```bash
streamlit run app.py
```
By default, the web browser will open to:
`http://localhost:8501`
