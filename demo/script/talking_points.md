# 🗣️ VoltAudit AI Launch Talking Points

Key talking points for live developer presentations and media showcases:

1. **Decoupled Security Boundaries:**
   - Mention that the backend does not connect directly to SQL. All operations route through isolated Model Context Protocol (MCP) tool interfaces.
   - Explain how this model prevents SQL injection and boundaries traversal when parsing untrusted invoices.

2. **Specialized AI Agents:**
   - Explain that each of the eight agents has a specific role (ingestion, rates, peaking, math, anomalies, risk, reports, and coordination).
   - This ensures the LLM is focused on a narrow task context rather than trying to perform a complex audit in a single run.

3. **Human-in-the-Loop Safeguard:**
   - Automatic payouts are blocked when compliance drops below 80%.
   - Valid justifications are verified by a governance override check.

4. **SRE and Operational Integrity:**
   - The platform has passed pre-commit gates, strict static analysis, and concurrent load tests (>20 parallel pipelines/sec).
