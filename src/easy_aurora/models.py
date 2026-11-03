"""Pydantic models for structured LLM outputs."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Summary(BaseModel):
    """A structured summary of text."""

    title: str = Field(description="Short title for the content")
    key_points: list[str] = Field(description="3-5 key points")
    sentiment: str = Field(description="Overall sentiment: positive, neutral, or negative")


class ChatMessage(BaseModel):
    """A single chat message."""

    role: str
    content: str
