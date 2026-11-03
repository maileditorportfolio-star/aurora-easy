"""Unified LLM client supporting multiple providers."""

from __future__ import annotations

from typing import Any

from .config import get_settings
from .models import ChatMessage


class LLMClient:
    """Thin wrapper around Anthropic / OpenAI chat completions."""

    def __init__(self, provider: str | None = None, model: str | None = None):
        settings = get_settings()
        self.provider = provider or settings.default_provider
        self.model = model or settings.default_model
        self._client: Any = None
        self._init_client(settings)

    def _init_client(self, settings: Any) -> None:
        if self.provider == "anthropic":
            import anthropic

            self._client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
        elif self.provider == "openai":
            import openai

            self._client = openai.OpenAI(api_key=settings.openai_api_key)
        else:
            raise ValueError(f"Unknown provider: {self.provider}")

    def chat(self, messages: list[ChatMessage], **kwargs: Any) -> str:
        """Send messages and return the assistant's text response."""
        if self.provider == "anthropic":
            anthropic_messages = [{"role": m.role, "content": m.content} for m in messages]
            response = self._client.messages.create(
                model=self.model,
                max_tokens=kwargs.get("max_tokens", 1024),
                messages=anthropic_messages,
            )
            return response.content[0].text
        if self.provider == "openai":
            openai_messages = [{"role": m.role, "content": m.content} for m in messages]
            response = self._client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                max_tokens=kwargs.get("max_tokens", 1024),
            )
            return response.choices[0].message.content or ""
        raise ValueError(f"Unknown provider: {self.provider}")

    def summarize(self, text: str) -> dict[str, Any]:
        """Return a structured summary of the given text."""
        from pydantic import TypeAdapter

        from .models import Summary

        adapter = TypeAdapter(Summary)
        schema = adapter.json_schema()
        prompt = (
            f"Summarize the following text and return JSON matching this schema:\n"
            f"{schema}\n\nText:\n{text}"
        )
        messages = [ChatMessage(role="user", content=prompt)]
        raw = self.chat(messages)
        return adapter.validate_json(raw).model_dump()
