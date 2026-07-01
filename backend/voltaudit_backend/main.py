from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="VoltAudit AI API",
    description="Enterprise AI Workforce for Intelligent Invoice Auditing",
    version="0.1.0",
)

# CORS configurations
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # nosemgrep
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root() -> dict[str, str]:
    """Returns a basic Welcome message."""
    return {"message": "Welcome to VoltAudit AI API Services"}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Returns the api system health status."""
    return {"status": "healthy"}
