"""Retrieval logic combining vector store + embedder."""

from __future__ import annotations

from .chunker import Chunk
from .embeddings import Embedder
from .vector_store import VectorStore


class Retriever:
    def __init__(self, store: VectorStore, embedder: Embedder):
        self.store = store
        self.embedder = embedder

    def retrieve(self, query: str, top_k: int = 5) -> list[tuple[Chunk, float]]:
        qvec = self.embedder.embed([query])[0]
        # If TF-IDF embedder needs fitting, fit on stored chunks
        if not hasattr(self.embedder, "_fitted") or not getattr(self.embedder, "_fitted", True):
            texts = [c.text for c in self.store.chunks]
            if hasattr(self.embedder, "fit"):
                self.embedder.fit(texts + [query])
        qvec = self.embedder.embed([query])[0]
        return self.store.search(qvec, top_k=top_k)
