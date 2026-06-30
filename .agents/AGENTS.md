# 🤖 VoltAudit AI Workspace Rules for Agents

You are operating inside the **VoltAudit AI** repository. You must adhere to the following rules without exception.

---

## 🏛️ Invariants

1. **Spec-Driven Development:** Do not write code or create database schemas without an approved specification document located in `specs/`. If a change deviates from specifications, request confirmation or update the spec first.
2. **Strict Quality Gates:** Before completing any implementation task, you MUST run:
   - `uv run ruff check . --fix`
   - `uv run ruff format .`
   - `uv run mypy .`
   - `uv run pytest`
   Ensure all check passes with exit code `0`.
3. **No Hardcoded Secrets:** You must never write credentials, tokens, or API keys directly in files. Check configuration values against `.env.example` and place them strictly in environment variables.
4. **Decoupled Architecture:** Keep `backend`, `frontend`, `agents`, and `mcp` separate. Do not import backend files inside the frontend or create cross-boundary imports.

---

## 💻 Style Rules

- **Python:** Use strict PEP 8 type hints and Google-style docstrings for all functions, modules, and classes.
- **TypeScript/React:** Avoid the `any` type. Use explicit interface declarations for component props and state variables.
- **Modularity:** Register compliance rules or invoice parsing algorithms as separate modules that implement defined interfaces.

---

## ⚡ Git Commits

Follow Conventional Commits format when staging changes:
- `feat(component): description` for new capabilities.
- `fix(component): description` for bugs.
- Use `git status` and verify that no cache directories (`.venv`, `node_modules`, `__pycache__`) or local `.env` configuration files are staged.
