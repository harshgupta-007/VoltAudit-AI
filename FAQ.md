# Frequently Asked Questions (FAQ)

Here are the most frequently asked questions regarding VoltAudit AI.

---

## 1. What is the difference between ADK and MCP?
- **Agent Development Kit (ADK):** Orchestrates the high-level workforce loop, manages agent context states, handles prompt injections, and checks tool permissions.
- **Model Context Protocol (MCP):** Connects the agent to infrastructure (databases, local files) in a Zero-Trust manner by serving schema-validated tools.

---

## 2. Why does the system use SQLite?
SQLite is selected for portability, local container reproducibility, and zero-configuration development. To ensure concurrent reliability, connections are immediately closed in `finally` blocks.

---

## 3. Can I run the application without Docker?
Yes! You can run the application directly using Python `uv`:
1. Start the FastAPI backend:
   ```bash
   cd backend && uv run uvicorn voltaudit_backend.main:app
   ```
2. Start the Streamlit dashboard:
   ```bash
   cd frontend && uv run streamlit run app.py
   ```
Both applications resolve project roots dynamically.
