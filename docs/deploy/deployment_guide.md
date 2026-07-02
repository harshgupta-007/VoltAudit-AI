# 🚀 VoltAudit AI Deployment & CI/CD Guide

This guide provides instructions on containerizing, deploying, and releasing VoltAudit AI.

---

## 1. Local Container Development (Docker & Docker Compose)

To build and run all services locally inside isolated containers:

### 1. Build and Run Services
Run this command from the root of the workspace:
```bash
docker compose -f deploy/docker-compose.yml up --build
```

### 2. Verify Port Endpoints
- **FastAPI Application Layer:** `http://localhost:8000/health`
- **Streamlit Frontend:** `http://localhost:8501`

### 3. Tear Down Container Deployments
```bash
docker compose -f deploy/docker-compose.yml down -v
```

---

## 2. Cloud Deployment (Google Cloud Run)

To deploy services to production Google Cloud Run:

### 1. Build and Push Backend Image to Google Artifact Registry
```bash
docker build -t gcr.io/voltaudit-production/backend:latest -f deploy/Dockerfile.backend .
docker push gcr.io/voltaudit-production/backend:latest
```

### 2. Deploy Backend Container Service
```bash
gcloud run deploy voltaudit-backend \
    --image gcr.io/voltaudit-production/backend:latest \
    --platform managed \
    --allow-unauthenticated \
    --port 8000 \
    --set-env-vars ENV=production,LOG_LEVEL=INFO
```

### 3. Build and Deploy Streamlit Frontend
```bash
docker build -t gcr.io/voltaudit-production/frontend:latest -f deploy/Dockerfile.frontend .
docker push gcr.io/voltaudit-production/frontend:latest

gcloud run deploy voltaudit-frontend \
    --image gcr.io/voltaudit-production/frontend:latest \
    --platform managed \
    --allow-unauthenticated \
    --port 8501 \
    --set-env-vars API_BASE_URL=https://<your-backend-cloudrun-url>/api/v1
```

---

## 3. CI/CD Pipeline Configuration (GitHub Actions)

A GitHub Actions workflow script is configured under `.github/workflows/ci.yml`. On every pull request or commit to master, the pipeline automatically:
1. Provisions an Ubuntu Runner environment.
2. Checks out codebase version trees.
3. Installs Astral `uv` Python package manager.
4. Synchronizes virtual environments.
5. Runs `ruff format` and `ruff check`.
6. Executes type checks via `mypy`.
7. Triggers the pytest test suite (unit and integration tests).
8. Performs static security scans using custom Semgrep policies.
