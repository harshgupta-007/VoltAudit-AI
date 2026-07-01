"""Configuration settings for the VoltAudit Streamlit Frontend."""

import os


class FrontendSettings:
    """Frontend configurations referencing application service targets."""

    API_BASE_URL: str = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")


settings = FrontendSettings()
