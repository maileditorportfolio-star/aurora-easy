"""Tests for Easy Aurora."""

from __future__ import annotations

from easy_aurora.config import Settings


def test_settings_defaults() -> None:
    s = Settings()
    assert s.default_provider == "anthropic"


def test_settings_custom() -> None:
    s = Settings()
    s.default_provider = "openai"
    assert s.default_provider == "openai"
