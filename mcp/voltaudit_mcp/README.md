# 🔌 VoltAudit AI Model Context Protocol (MCP) Server

This directory contains the production-grade **Enterprise MCP Platform** implementation for VoltAudit AI, built using Anthropic's FastMCP SDK. It serves as the exclusive tool interface for all specialized AI workers, ensuring complete separation of concerns and least-privilege resource access.

---

## 1. Domain Registry

The platform exposes 6 logical domains:

1. **Document Services (MCP-DOM-001):** Restricts file reading boundaries to prevent directory traversal attacks.
2. **Vendor Services (MCP-DOM-002):** Resolves raw vendor strings against canonical supplier profiles.
3. **Contract & PO Services (MCP-DOM-003):** Indexes active rates sheets and PO fund allocations.
4. **Meter Readings Services (MCP-DOM-004):** Reconciles generation metrics with plant operations logs.
5. **Audit & Discrepancy Services (MCP-DOM-005):** Persists risk scores, outcomes, and discrepancies.
6. **Notification Services (MCP-DOM-006):** Dispatches critical alerts to operator gateways.

---

## 2. Tool Catalogue

The following 9 tools are exposed over JSON-RPC stdio channels:

* **`read_uploaded_file` (MCP-TOOL-001):** Load invoice text content.
* **`search_canonical_vendors` (MCP-TOOL-002):** Query supplier names.
* **`query_active_contracts` (MCP-TOOL-003):** Query rate schedules.
* **`query_purchase_orders` (MCP-TOOL-004):** Query PO budgets.
* **`lookup_meter_readings` (MCP-TOOL-005):** Query generation volumes.
* **`save_audit_run` (MCP-TOOL-006):** Write run metrics.
* **`create_discrepancy_records` (MCP-TOOL-007):** Write warning details.
* **`query_invoice_history` (MCP-TOOL-008):** Query billing duplicates.
* **`notify_human_operator` (MCP-TOOL-009):** Alert accounts payable.

---

## 3. Developer & Extensions Guide

### Adding a New Tool
1. **Define Schema:** Add a Pydantic model for input parameters in `server.py`.
2. **Register Tool:** Use the `@mcp.tool()` decorator:
   ```python
   @mcp.tool("MCP-TOOL-010")
   def new_utility_action(param: str) -> str:
       # Parameterized executions
       return json.dumps({"status": "completed"})
   ```
3. **Write Unit Tests:** Add a verification case to `tests/unit/test_mcp.py`.

---

## 4. Operational Troubleshooting

* **Permission Denied (Path Traversal):** Ensure the requested file ID resides strictly under `backend/data/uploads`.
* **Database Queries Blocked:** Check SQLite database locks on `voltaudit.db`. Run `python -m voltaudit_mcp.database` to re-seed mock data.
