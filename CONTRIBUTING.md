# Contributing to VoltAudit AI

We welcome contributions to VoltAudit AI! Please follow these guidelines to ensure code quality and consistency.

---

## 1. Development Workflow

1. **Fork the Repository:** Create a personal fork of the repository.
2. **Branch Naming:** Create a branch following conventional formats:
   - `feat/feature-name` for new capabilities.
   - `fix/bug-fix` for security patches or fixes.
3. **Branch Target:** Always branch off and target `master` (or `main`).

---

## 2. Coding & Quality Standards

Before submitting a Pull Request, you must verify:
- **Formatting:** Code must be formatted with Ruff:
  ```bash
  uv run ruff format .
  ```
- **Linting:** Ensure zero errors or warnings:
  ```bash
  uv run ruff check . --fix
  ```
- **Type Safety:** Maintain strict Mypy types:
  ```bash
  uv run mypy .
  ```
- **Tests:** All tests must pass:
  ```bash
  uv run pytest
  ```

---

## 3. Pre-commit Hooks

Ensure pre-commit hooks are installed and pass on every commit:
```bash
uv run pre-commit install
uv run pre-commit run --all-files
```

---

## 4. Commit Message Formats

We enforce Conventional Commit conventions for all messages:
- `feat(component): added new skill tracer`
- `fix(security): resolved path traversal checks`
