# 🤝 Contribution Guidelines

This document outlines the workflow for contributing code changes to the VoltAudit AI repository. All developers (human and agentic) must follow this process to maintain a clean codebase history and ensure code quality.

---

## 🌿 Git Branching Strategy

We use a feature-branch workflow. All active development occurs on dedicated branches that target the `main` branch.

### Branch Naming Conventions
- **Feature Development:** `feat/issue-number-short-description` (e.g. `feat/102-invoice-ocr-parser`)
- **Bug Fixes:** `fix/issue-number-short-description` (e.g. `fix/99-date-timezone-offset`)
- **Refactoring:** `refactor/short-description` (e.g. `refactor/cleanup-db-sessions`)
- **Documentation:** `docs/short-description` (e.g. `docs/add-api-endpoints`)
- **CI/CD or Infrastructure:** `infra/short-description` (e.g. `infra/configure-github-actions`)

---

## 📝 Commit Message Standards

We follow the **Conventional Commits** specification. This format helps generate automated changelogs and enforces clear commit discipline.

### Commit Format
```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

### Types
- **`feat`**: A new feature (corresponds to a minor release).
- **`fix`**: A bug fix (corresponds to a patch release).
- **`docs`**: Documentation-only changes.
- **`style`**: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc.).
- **`refactor`**: A code change that neither fixes a bug nor adds a feature.
- **`perf`**: A code change that improves performance.
- **`test`**: Adding missing tests or correcting existing tests.
- **`chore`**: Changes to the build process, auxiliary tools, or libraries.

### Example Commits
* `feat(backend): add invoice ingestion endpoint supporting PDF uploads`
* `fix(parser): prevent out-of-bounds error on single-item invoice grids`
* `docs(readme): correct step-by-step instructions for uv install`

---

## 🔄 Pull Request Workflow

### 1. Preparation
Before submitting a Pull Request (PR):
- Rebase your branch onto the latest `main`:
  ```bash
  git fetch origin
  git rebase origin/main
  ```
- Run the local validation suite:
  ```bash
  uv run ruff check .
  uv run ruff format .
  uv run mypy .
  uv run pytest
  ```

### 2. Submission
- Open a Pull Request on GitHub.
- Use a descriptive title and fill out the PR Template (detailing the changes, issues fixed, and verification steps).
- Ensure the CI system executes and all quality gates pass (linter, format, type-check, tests, and Semgrep security scan).

### 3. Peer Review
- At least one code owner or team member must review and approve the PR.
- Address review feedback by adding commits to your branch.
- Once approved and CI passes, the branch will be squashed and merged into `main`.
