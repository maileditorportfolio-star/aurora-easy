# Easy Aurora

A Python starter repository for building AI-powered applications.

## Features

- Python 3.11+ with modern tooling (`uv`, `ruff`, `pytest`)
- Multi-provider LLM support (Anthropic, OpenAI) via a unified client
- Pydantic-based structured outputs
- Environment-based configuration
- Pre-commit hooks with secret scanning

## Quick Start

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your API keys

# Run tests
uv run pytest

# Run the example
uv run python -m easy_aurora
```

## Project Structure

```
src/easy_aurora/
├── config.py       # Environment & settings
├── llm.py          # LLM client wrapper
├── models.py       # Pydantic schemas
└── __main__.py     # Entry point
```

## License

MIT
