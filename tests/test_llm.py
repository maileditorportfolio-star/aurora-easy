"""Tests for LLMClient."""

from unittest.mock import MagicMock, patch

from easy_aurora.llm import LLMClient
from easy_aurora.models import ChatMessage


def test_llm_chat_anthropic():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="Hello there!")]
    mock_client.messages.create.return_value = mock_response

    with patch("anthropic.Anthropic", return_value=mock_client):
        client = LLMClient(provider="anthropic", model="claude-test")
        client._client = mock_client
        msgs = [ChatMessage(role="user", content="hi")]
        reply = client.chat(msgs)
        assert reply == "Hello there!"


def test_llm_chat_openai():
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="Hi!"))]
    mock_client.chat.completions.create.return_value = mock_response

    with patch("openai.OpenAI", return_value=mock_client):
        client = LLMClient(provider="openai", model="gpt-test")
        client._client = mock_client
        msgs = [ChatMessage(role="user", content="hi")]
        reply = client.chat(msgs)
        assert reply == "Hi!"
