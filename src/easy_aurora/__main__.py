"""Package entry point."""

from __future__ import annotations

from .config import get_settings
from .llm import LLMClient
from .models import ChatMessage


def main() -> None:
    settings = get_settings()
    settings.validate()
    client = LLMClient()
    messages = [ChatMessage(role="user", content="Say hello in one sentence.")]
    reply = client.chat(messages)
    print(reply)


if __name__ == "__main__":
    main()
