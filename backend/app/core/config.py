from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.ai.types import AIProvider


BACKEND_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    app_name: str = "Bridge AI"
    app_version: str = "0.1.0"
    app_description: str = (
        "AI-powered operations infrastructure for community organizations."
    )

    environment: Literal[
        "development",
        "testing",
        "production",
    ] = "development"

    debug: bool = True
    api_v1_prefix: str = "/api/v1"

    allowed_origins: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    database_url: str = "sqlite:///./bridge_ai.db"
    database_echo: bool = False

    # AI
    ai_provider: AIProvider = AIProvider.FAKE
    ai_model: str = "fake-document-analyzer-v1"
    anthropic_api_key: str | None = None

    # Documents
    document_max_upload_bytes: int = 5_000_000
    ai_max_document_characters: int = 50_000

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("DATABASE_URL must not be empty")

        return value


@lru_cache
def get_settings() -> Settings:
    return Settings()