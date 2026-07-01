"""FastAPI application entrypoint for VoltAudit AI."""

import time
import uuid
from collections.abc import Awaitable, Callable

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from voltaudit_backend.config import settings
from voltaudit_backend.router import router
from voltaudit_backend.schemas import HealthStatus

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Enterprise AI Workforce for Intelligent Invoice Auditing",
    version="0.1.0",
)


class CorrelationIDMiddleware(BaseHTTPMiddleware):
    """Middleware for injecting unique correlation IDs to trace requests."""

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        # Check if incoming request already has a correlation header
        correlation_id = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())

        # Inject into request state for logs access
        request.state.correlation_id = correlation_id

        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time

        # Inject into response headers
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Response-Time-Seconds"] = f"{duration:.4f}"

        return response


# Apply CORS and Correlation Middlewares
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # nosemgrep
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(CorrelationIDMiddleware)

# Register audit router
app.include_router(router, prefix=settings.API_PREFIX)


# System Health endpoints
@app.get("/health", response_model=HealthStatus, tags=["Health"])
def health_check() -> HealthStatus:
    """Return basic health liveness checks."""
    return HealthStatus(status="OK", version="0.1.0", mcp_connection=True)


@app.get("/ready", response_model=HealthStatus, tags=["Health"])
def readiness_check() -> HealthStatus:
    """Return readiness confirmations for downstream system interfaces."""
    # Verify local uploads folder is writable
    is_ready = settings.UPLOAD_DIR.exists()
    return HealthStatus(
        status="READY" if is_ready else "ERROR", version="0.1.0", mcp_connection=True
    )


@app.get("/live", response_model=HealthStatus, tags=["Health"])
def liveness_check() -> HealthStatus:
    """Simple status liveness verification."""
    return HealthStatus(status="ALIVE", version="0.1.0", mcp_connection=True)


@app.get("/")
def read_root() -> dict[str, str]:
    """Returns a basic Welcome message."""
    return {"message": "Welcome to VoltAudit AI API Services"}
