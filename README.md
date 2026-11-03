# Easy Aurora — Document Q&A / RAG

A Python RAG (Retrieval-Augmented Generation) system for internal knowledge bases and customer support bots.

## Features

- **Document ingestion**: PDF, DOCX, TXT, Markdown
- **Chunking** with overlap for better retrieval
- **Embeddings**: TF-IDF (offline) or OpenAI embeddings
- **Vector store**: in-memory with cosine similarity, persisted to JSON
- **LLM generation**: Anthropic or OpenAI
- **FastAPI** REST API with ecommerce1-style envelope (`{success, data, message, details}`)
- Structured logging (structlog), Pydantic validation, pre-commit hooks

## Quick Start

```bash
# Install dependencies (locked)
uv sync --extra dev

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run tests
uv run pytest

# Lint
uv run ruff check .

# Start the API server
uv run python -m easy_aurora --serve
# API at http://localhost:8000, docs at /docs

# Or run with Docker
docker build -t easy-aurora .
docker run -p 8000:8000 --env-file .env easy-aurora
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/documents/upload` | Upload a document (PDF/DOCX/TXT/MD) |
| POST | `/query` | Ask a question over ingested docs |
| DELETE | `/documents` | Clear all documents |

## Example

```bash
# Upload a document
curl -X POST http://localhost:8000/documents/upload -F "file=@docs/manual.pdf"

# Query
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" \
  -d '{"question": "What is the return policy?"}'
```

## Project Structure

```
src/easy_aurora/
├── api/            # FastAPI app + envelope
├── config.py       # Environment & settings
├── ingestion/      # Document loaders
├── llm.py          # LLM client wrapper
├── models.py       # Pydantic schemas
├── rag/            # Chunker, embeddings, vector store, retriever, pipeline
└── utils/          # Logging
```

## License

MIT
