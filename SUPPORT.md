# VoltAudit AI Support Guide

Get help, troubleshoot issues, and contact the maintenance team.

---

## 1. Support Channels

- **GitHub Issues:** Use GitHub Issues exclusively to report bugs, request features, or propose improvements.
- **Discussions Forum:** Ask general usage questions or discuss design ideas in the GitHub Discussions tab.
- **Email Support:** For commercial support or private security queries, email `support@voltaudit.com`.

---

## 2. Common Troubleshooting Steps

### 1. Database Locking Errors
If SQLite complains about locked connection states:
- Terminate any hung FastAPI application servers.
- Ensure the application is closing connections in `finally` blocks.

### 2. ModuleNotFoundError on Import
If python fails to find packages (e.g. `voltaudit_agents` or `spk_007_risk_scorer`):
- Ensure you run applications using `uv run`.
- Confirm your PYTHONPATH environment variable or directory appends resolve to the project root.
