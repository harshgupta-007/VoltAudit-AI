# 📘 VoltAudit AI Operational Runbook & disaster Recovery

This operations manual details runbooks, backup schedules, and recovery patterns for VoltAudit AI.

---

## 1. System Maintenance & Diagnostics

### FastAPI Backend App Service
* **Diagnostic Check:** Verify port availability (default: `8000`).
* **Command:** `curl -s http://localhost:8000/health`
* **Expected Result:** `{"status": "OK", "version": "0.1.0", "mcp_connection": true}`

### Streamlit UI Service
* **Diagnostic Check:** Verify browser accessibility.
* **Port:** `8501` (Default)
* **Command:** `curl -s http://localhost:8501`

---

## 2. Backup Strategy

The system utilizes an SQLite relational database stored at `mcp/voltaudit_mcp/voltaudit.db`.

### 1. Database Backup Schedule
* **Interval:** Daily incremental backups; weekly full backups.
* **Retention Policy:**
  - Keep daily backups for 14 days.
  - Keep weekly backups for 90 days.
  - Keep monthly archives for 1 year.

### 2. Manual Backup Trigger
```bash
sqlite3 mcp/voltaudit_mcp/voltaudit.db ".backup 'mcp/voltaudit_mcp/voltaudit_backup_$(date +%F).db'"
```

### 3. Restore Strategy
In the event of database corruption:
1. Stop the FastAPI application.
2. Archive the corrupted database file.
3. Copy the latest valid backup file to `mcp/voltaudit_mcp/voltaudit.db`.
4. Restart the FastAPI application.

---

## 3. Disaster Recovery (DR)

### Recovery Time Objective (RTO)
* **Target:** Under 15 minutes for application and database restores.

### Recovery Point Objective (RPO)
* **Target:** Under 24 hours (maximum data loss limited to the last daily snapshot).
