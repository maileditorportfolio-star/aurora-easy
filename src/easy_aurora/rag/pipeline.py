"""End-to-end RAG pipeline: ingest + query."""

from __future__ import annotations

from pathlib import Path

from ..llm import LLMClient
from ..models import ChatMessage
from .chunker import chunk_text
from .embeddings import Embedder, TfidfEmbedder
from .retriever import Retriever
from .vector_store import VectorStore


class RagPipeline:
    def __init__(
        self,
        store_path: str | Path | None = None,
        embedder: Embedder | None = None,
        llm: LLMClient | None = None,
    ):
        self.store = VectorStore(store_path)
        self.embedder = embedder or TfidfEmbedder()
        self.llm = llm or LLMClient()
        self.retriever = Retriever(self.store, self.embedder)

    def ingest(self, path: str | Path, metadata: dict[str, str] | None = None) -> int:
        from ..ingestion.loaders import load_text

        text = load_text(path)
        chunks = chunk_text(text, metadata=metadata or {"source": str(path)})
        if not chunks:
            return 0
        # Fit TF-IDF if needed
        if isinstance(self.embedder, TfidfEmbedder):
            texts = [c.text for c in self.store.chunks] + [c.text for c in chunks]
            self.embedder.fit(texts)
        vectors = self.embedder.embed([c.text for c in chunks])
        self.store.add(chunks, vectors)
        return len(chunks)

    def query(self, question: str, top_k: int = 5) -> dict:
        # Ensure TF-IDF fitted
        if isinstance(self.embedder, TfidfEmbedder) and self.store.chunks:
            texts = [c.text for c in self.store.chunks]
            self.embedder.fit(texts)
        results = self.retriever.retrieve(question, top_k=top_k)
        context = "\n\n".join(c.text for c, _ in results)
        prompt = (
            "Answer the question using only the provided context. "
            "If the answer is not in the context, say you don't know.\n\n"
            f"Context:\n{context}\n\nQuestion: {question}"
        )
        messages = [ChatMessage(role="user", content=prompt)]
        answer = self.llm.chat(messages)
        sources = [{"text": c.text[:200], "score": s, "metadata": c.metadata} for c, s in results]
        return {"answer": answer, "sources": sources}
