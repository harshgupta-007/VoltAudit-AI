# 🎙️ VoltAudit AI Demo Script, Storyboard & Voice-Over Guide

This package guides you through presenting a professional 5-minute demo of VoltAudit AI.

---

## 1. Demo Storyboard

| Slide/Screen | Visual Layout | Audio / Voice-over Script | Timing |
| :--- | :--- | :--- | :--- |
| **1. Intro** | Title slide: "VoltAudit AI - Bounded Agentic Auditing" | "Welcome. Today we're demonstrating VoltAudit AI, a cooperative multi-agent system designed to audit complex enterprise utility invoices." | 0:00 - 0:45 |
| **2. Problem** | Standard invoice with Peak Tariff errors and duplicated items | "Enterprise utility invoices are subject to tariff violations, rate calculation mistakes, and duplicate billings, leading to major cost leaks." | 0:45 - 1:30 |
| **3. Architecture** | Sequence diagram of ADK Agent Workforce and MCP boundaries | "To solve this securely, VoltAudit AI separates concerns. Our 8 specialized agents communicate with SQL databases exclusively using Model Context Protocol." | 1:30 - 2:30 |
| **4. Live Demo** | Streamlit UI: upload `google-dirty.txt`, click run | "Let's upload a dirty invoice. The dashboard displays the live execution steps as each agent checks ingestion, contracts, tariffs, and anomalies." | 2:30 - 4:00 |
| **5. Result** | Compliance scorecard (70/100) and human override gate | "The run yields a compliance score of 70/100. Because a discrepancy was flagged, the payment is blocked until an auditor inputs a justification." | 4:00 - 5:00 |

---

## 2. Key Talking Points

- **Zero-Trust Tool Boundary:** Bounded MCP tool executions prevent LLMs from running raw database insertions or deletes.
- **Stateless Composition:** Separating agent logic from math calculations ensures that calculations remain deterministic.
- **Traceability:** Unique Correlation IDs trace operations from client upload through agent logic to MCP queries.

---

## 3. Recording Checklist

- [ ] Select wide screen layout (e.g. 1080p resolution).
- [ ] Verify FastAPI is running on port `8000`.
- [ ] Verify Streamlit is running on port `8501`.
- [ ] Prepare test files `google-clean.txt` and `google-dirty.txt`.
