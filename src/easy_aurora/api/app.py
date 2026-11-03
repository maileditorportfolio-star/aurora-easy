"""FastAPI application with RAG endpoints."""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from ..api.envelope import fail, ok
from ..config import get_settings
from ..rag.pipeline import RagPipeline
from ..utils.logging import configure_logging, get_logger

configure_logging()
logger = get_logger("api")

app = FastAPI(title="Easy Aurora RAG", version="0.1.0")

_pipeline: RagPipeline | None = None


def get_pipeline() -> RagPipeline:
    global _pipeline
    if _pipeline is None:
        settings = get_settings()
        settings.validate()
        _pipeline = RagPipeline(store_path=Path("data/store.json"))
    return _pipeline


class QueryRequest(BaseModel):
    question: str
    top_k: int = 5


@app.get("/health")
def health():
    return ok({"status": "ok"})


@app.post("/documents/upload")
def upload_document(file: UploadFile = File(...)):  # noqa: B008
    upload_dir = Path("data/uploads")
    upload_dir.mkdir(parents=True, exist_ok=True)
    dest = upload_dir / (file.filename or "upload.txt")
    content = file.file.read()
    dest.write_bytes(content)
    pipeline = get_pipeline()
    count = pipeline.ingest(dest, metadata={"source": file.filename or ""})
    logger.info("document_ingested", filename=file.filename, chunks=count)
    return ok({"filename": file.filename, "chunks": count})


@app.post("/query")
def query(req: QueryRequest):
    if not req.question.strip():
        raise HTTPException(status_code=400, detail=fail("Question cannot be empty"))
    pipeline = get_pipeline()
    result = pipeline.query(req.question, top_k=req.top_k)
    return ok(result)


@app.delete("/documents")
def clear_documents():
    pipeline = get_pipeline()
    pipeline.store.clear()
    return ok({"message": "All documents cleared"})
