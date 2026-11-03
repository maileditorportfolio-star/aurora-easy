"""Document loaders for various file formats."""

from __future__ import annotations

from pathlib import Path

from docx import Document as DocxDocument
from pypdf import PdfReader


def load_text(path: str | Path) -> str:
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".pdf":
        reader = PdfReader(str(p))
        return "\n".join(page.extract_text() or "" for page in reader.pages)
    if suffix == ".docx":
        doc = DocxDocument(str(p))
        return "\n".join(para.text for para in doc.paragraphs)
    # txt, md, etc.
    return p.read_text(encoding="utf-8", errors="ignore")
