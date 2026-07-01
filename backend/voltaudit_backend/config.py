"""Configuration management settings for the VoltAudit Backend API."""

from pathlib import Path

from pydantic import BaseModel


class Settings(BaseModel):
    """System-wide configuration settings with secure defaults."""

    # API configuration
    API_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "VoltAudit AI API"
    DEBUG: bool = False

    # Directories
    BASE_DIR: Path = Path(__file__).resolve().parents[2]
    UPLOAD_DIR: Path = BASE_DIR / "backend" / "data" / "uploads"

    def create_directories(self) -> None:
        """Create base directory folders if missing."""
        self.UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


# Initialize global settings
settings = Settings()
settings.create_directories()
