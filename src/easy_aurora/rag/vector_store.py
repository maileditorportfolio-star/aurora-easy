"""In-memory vector store with cosine similarity search."""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from .chunker import Chunk


class VectorStore:
    def __init__(self, path: str | Path | None = None):
        self.path = Path(path) if path else None
        self.vectors: np.ndarray | None = None
        self.chunks: list[Chunk] = []
        if self.path and self.path.exists():
            self._load()

    def add(self, chunks: list[Chunk], vectors: np.ndarray) -> None:
        self.chunks.extend(chunks)
        if self.vectors is None:
            self.vectors = vectors
        else:
            self.vectors = np.vstack([self.vectors, vectors])
        if self.path:
            self._save()

    def search(self, query_vec: np.ndarray, top_k: int = 5) -> list[tuple[Chunk, float]]:
        if self.vectors is None or len(self.chunks) == 0:
            return []
        q = query_vec.reshape(1, -1)
        norms = np.linalg.norm(self.vectors, axis=1, keepdims=True) + 1e-12
        qnorm = np.linalg.norm(q) + 1e-12
        sims = (self.vectors / norms) @ (q.T / qnorm)
        sims = sims.flatten()
        order = np.argsort(sims)[::-1][:top_k]
        return [(self.chunks[i], float(sims[i])) for i in order]

    def _save(self) -> None:
        assert self.path is not None
        self.path.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "chunks": [{"text": c.text, "metadata": c.metadata} for c in self.chunks],
            "vectors": self.vectors.tolist() if self.vectors is not None else [],
        }
        self.path.write_text(json.dumps(data), encoding="utf-8")

    def _load(self) -> None:
        assert self.path is not None
        data = json.loads(self.path.read_text(encoding="utf-8"))
        from .chunker import Chunk

        self.chunks = [Chunk(text=d["text"], metadata=d["metadata"]) for d in data["chunks"]]
        if data["vectors"]:
            self.vectors = np.array(data["vectors"], dtype=np.float32)
        else:
            self.vectors = None

    def clear(self) -> None:
        self.chunks = []
        self.vectors = None
        if self.path and self.path.exists():
            self.path.unlink()
