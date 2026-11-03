FROM python:3.11-slim

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src/ ./src/

RUN pip install --no-cache-dir uv && uv sync --no-dev

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "easy_aurora.api.app:app", "--host", "0.0.0.0", "--port", "8000"]
