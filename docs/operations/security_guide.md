# 🛡️ VoltAudit AI Security Guide & Risk Register

This document outlines the security playbook, incident response, risk register, and compliance checklist for VoltAudit AI.

---

## 1. Incident Response Guide

In the event of a security anomaly or breach detection:

### Phase 1: Identification & Alerting
- Monitor API logs for HTTP 403/401 errors or prompt injection security violations.
- Verify logs of blocked prompt injections containing: `"action": "security_violation"`.

### Phase 2: Containment
- If an active threat is identified (e.g. malformed files traversing folders), isolate the affected API instance.
- Revoke API tokens and block traffic to IP addresses originating the malicious payloads.

### Phase 3: Eradication
- Update custom Semgrep rules or validation regex patterns to capture the newly identified attack vectors.
- Purge any uploaded malicious files in `backend/data/uploads/`.

### Phase 4: Recovery
- Restore the database from the last valid daily backup.
- Verify system liveness and readiness endpoints.

---

## 2. Risk Register

| Risk ID | Description | Severity | Mitigation Strategy | Status |
| :--- | :--- | :--- | :--- | :--- |
| **RSK-001** | Prompt injection in utility invoices bypassing checks. | **High** | Layered validations on text blocks; early abort patterns. | **Mitigated** |
| **RSK-002** | Path traversal attacks opening files outside uploads. | **Medium** | Path traversal validation; strictly matching base names. | **Mitigated** |
| **RSK-003** | Concurrent lock contentions in SQLite. | **Medium** | Try/finally connection closures; fast timeout retries. | **Mitigated** |

---

## 3. Compliance Checklist

- [x] **Least Privilege Access:** Agents possess strictly bounded `allowed_mcp_tools` lists.
- [x] **Secrets Separation:** Credentials configured through environment variables.
- [x] **Data Ingestion Sanitation:** Uploaded file path traversals verified and blocked.
- [x] **Traceability:** Execution steps log timestamp, agent, action, and details.
