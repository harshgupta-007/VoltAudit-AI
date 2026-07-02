# Security Policy

VoltAudit AI is designed with a **Zero-Trust** security architecture. We take any potential vulnerability seriously.

---

## 1. Reporting a Vulnerability

If you discover a security vulnerability in this project:
1. **Do not open a public issue.**
2. Send a detailed report to `security@voltaudit.com` containing:
   - Steps to reproduce the issue.
   - Sample exploit payloads (if applicable).
   - Recommended mitigations.

Our team will respond to reports within 48 hours and coordinate a public advisory if necessary.

---

## 2. Supported Versions

Security updates are actively applied to the following release branches:

| Version | Supported |
| :--- | :--- |
| **v1.0.x** | Yes (Active) |
| **v0.9.x** | Security hotfixes only |

---

## 3. Bounded Security Invariants

All developers and runtime integrations must adhere to the following invariants:
- **No Hardcoded Secrets:** Static API keys, database credentials, or tokens are blocked by pre-commit scanners.
- **Model Context Protocol Bounding:** LLMs must never execute direct shell commands or connect directly to SQLite. Bounded MCP tools act as the exclusive runtime interface.
- **Input File Validation:** All uploaded invoices are processed using strictly sanitized paths to prevent traversal attempts outside bounded directories.
