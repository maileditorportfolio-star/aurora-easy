"""Tests for chunker."""

from easy_aurora.rag.chunker import chunk_text


def test_chunk_text_basic():
    text = "a" * 1000
    chunks = chunk_text(text, chunk_size=300, overlap=30)
    assert len(chunks) > 1
    assert all(c.text for c in chunks)


def test_chunk_text_empty():
    assert chunk_text("") == []
    assert chunk_text("   ") == []


def test_chunk_text_small():
    chunks = chunk_text("hello world", chunk_size=500)
    assert len(chunks) == 1
    assert chunks[0].text == "hello world"
