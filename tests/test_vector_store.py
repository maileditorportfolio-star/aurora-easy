"""Tests for vector store."""

import numpy as np

from easy_aurora.rag.chunker import Chunk
from easy_aurora.rag.vector_store import VectorStore


def test_vector_store_add_search():
    store = VectorStore()
    chunks = [Chunk(text="hello", metadata={}), Chunk(text="world", metadata={})]
    vecs = np.array([[1.0, 0.0], [0.0, 1.0]], dtype=np.float32)
    store.add(chunks, vecs)
    q = np.array([1.0, 0.0], dtype=np.float32)
    results = store.search(q, top_k=1)
    assert len(results) == 1
    assert results[0][0].text == "hello"


def test_vector_store_empty():
    store = VectorStore()
    q = np.array([1.0, 0.0], dtype=np.float32)
    assert store.search(q) == []
