# 🏁 Developer Onboarding Guide

Welcome to **VoltAudit AI**! This guide will help you set up your local development environment and run quality checks to verify your installation.

---

## 🛠️ Required Software

Ensure your local workstation has the following installed before bootstrapping the environment:
1. **Python 3.11 or higher**
2. **Node.js v18 or higher** (with `npm` or `pnpm` configured)
3. **Git**
4. **uv** (Extreme performance Python package manager)
   - To install `uv` on macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - To install `uv` on Windows (PowerShell): `irm https://astral.sh/uv/install.ps1 | iex`

---

## ⚙️ Environment Setup

Follow these steps sequentially to configure the repository:

### 1. Synchronize Python Workspaces
From the root of the repository, execute:
```bash
# This creates a local virtual environment (.venv) and synchronizes all packages for the backend, agents, mcp, and tests.
uv sync
```

### 2. Configure Pre-commit Hooks
Register the pre-commit quality gates:
```bash
uv run pre-commit install
```
This ensures that every time you run `git commit`, your code is automatically checked for code style (Ruff), types (Mypy), and secrets leakage (detect-secrets).

### 3. Initialize Local Configuration
Copy the default environment variables template:
```bash
cp .env.example .env
```
Edit the newly created `.env` file and supply valid API keys and parameters (e.g., your Google Gemini API token).

---

## 🚀 Running the Local Environment

### 1. Running the Backend API
Navigate to the `backend/` directory and execute:
```bash
cd backend
uv run uvicorn src.main:app --reload
```
The API documentation will be available at `http://127.0.0.1:8000/docs`.

### 2. Running the Frontend Dashboard
Navigate to the `frontend/` directory, install Node modules, and run the Vite server:
```bash
cd frontend
npm install
npm run dev
```
The application will open at `http://localhost:3000`.

### 3. Running MCP Servers
To verify that Model Context Protocol (MCP) servers compile and run:
```bash
cd mcp
uv run python -m src.server
```

---

## 🛡️ Running Quality Checks locally

Before proposing a Pull Request, run the local quality checks manually to ensure everything passes the CI gates:

* **Format and Lint Code:**
  ```bash
  uv run ruff check . --fix
  uv run ruff format .
  ```
* **Strict Type Check:**
  ```bash
  uv run mypy .
  ```
* **Run Tests:**
  ```bash
  uv run pytest
  ```
* **Run Pre-Commit Hooks on All Files:**
  ```bash
  uv run pre-commit run --all-files
  ```

---

## 🔍 Troubleshooting

* **Python Virtual Environment Issue:** If your editor does not recognize types, configure your IDE to point to the `.venv` directory located at the root of the project.
* **Pre-commit Fails on detect-secrets:** If you accidentally committed a dummy secret string (e.g. `secret_key`), the Yelp hook might block you. Either mock the value or update the baseline:
  ```bash
  uv run detect-secrets scan > .secrets.baseline
  ```
