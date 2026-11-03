"""Embedding providers for RAG."""

from __future__ import annotations

import os
from typing import Protocol

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer


class Embedder(Protocol):
    def embed(self, texts: list[str]) -> np.ndarray: ...


class TfidfEmbedder:
    """Offline TF-IDF based embedder (no external API)."""

    def __init__(self) -> None:
        self.vectorizer = TfidfVectorizer()
        self._fitted = False

    def fit(self, texts: list[str]) -> None:
        self.vectorizer.fit(texts)
        self._fitted = True

    def embed(self, texts: list[str]) -> np.ndarray:
        if not self._fitted:
            self.vectorizer.fit(texts)
            self._fitted = True
        return self.vectorizer.transform(texts).toarray().astype(np.float32)


class OpenAIEmbedder:
    """OpenAI text-embedding-3-small embedder."""

    def __init__(self, api_key: str | None = None, model: str = "text-embedding-3-small"):
        import openai

        self.client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY", ""))
        self.model = model

    def embed(self, texts: list[str]) -> np.ndarray:
        response = self.client.embeddings.create(model=self.model, input=texts)
        vectors = [d.embedding for d in response.data]
        return np.array(vectors, dtype=np.float32)


def get_embedder(provider: str = "tfidf", **kwargs: object) -> Embedder:
    if provider == "openai":
        return OpenAIEmbedder(**kwargs)  # type: ignore[arg-type]
    return TfidfEmbedder()
