"""Text chunking utilities for RAG ingestion."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Chunk:
    text: str
    metadata: dict[str, str]


def chunk_text(
    text: str,
    chunk_size: int = 500,
    overlap: int = 50,
    metadata: dict[str, str] | None = None,
) -> list[Chunk]:
    """Split text into overlapping chunks by character count."""
    if not text.strip():
        return []
    meta = metadata or {}
    chunks: list[Chunk] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + chunk_size, n)
        piece = text[start:end].strip()
        if piece:
            chunks.append(Chunk(text=piece, metadata=dict(meta)))
        if end >= n:
            break
        start = end - overlap
        if start < 0:
            start = 0
    return chunks
