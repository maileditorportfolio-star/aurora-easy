"""Configuration management for Easy Aurora."""

from __future__ import annotations

import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    anthropic_api_key: str = os.getenv("ANTHROPIC_API_KEY", "")
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    default_provider: str = os.getenv("DEFAULT_PROVIDER", "anthropic")
    default_model: str = os.getenv("DEFAULT_MODEL", "claude-sonnet-4-20250514")

    def validate(self) -> None:
        """Raise if required keys are missing for the chosen provider."""
        if self.default_provider == "anthropic" and not self.anthropic_api_key:
            raise ValueError("ANTHROPIC_API_KEY is required when provider is 'anthropic'")
        if self.default_provider == "openai" and not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when provider is 'openai'")


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
