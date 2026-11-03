"""Tests for RagPipeline."""

from unittest.mock import MagicMock

from easy_aurora.llm import LLMClient
from easy_aurora.rag.pipeline import RagPipeline


def test_pipeline_ingest_and_query(tmp_path):
    store_path = tmp_path / "store.json"
    llm = MagicMock(spec=LLMClient)
    llm.chat.return_value = "The answer is 42."
    pipeline = RagPipeline(store_path=store_path, llm=llm)

    doc = tmp_path / "doc.txt"
    doc.write_text("The meaning of life is 42. Always remember this.")
    count = pipeline.ingest(doc)
    assert count >= 1

    result = pipeline.query("What is the meaning of life?")
    assert "answer" in result
    assert "sources" in result
    assert result["answer"] == "The answer is 42."
    assert len(result["sources"]) >= 1


def test_pipeline_query_empty_store(tmp_path):
    store_path = tmp_path / "store.json"
    llm = MagicMock(spec=LLMClient)
    llm.chat.return_value = "I don't know."
    pipeline = RagPipeline(store_path=store_path, llm=llm)
    result = pipeline.query("anything")
    assert "answer" in result
