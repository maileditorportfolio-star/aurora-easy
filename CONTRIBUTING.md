# Contributing

1. Fork and clone the repo.
2. Install: `uv sync --extra dev`
3. Create a branch: `git checkout -b feat/your-feature`
4. Make changes with tests.
5. Run: `uv run ruff check . && uv run pytest`
6. Commit with Conventional Commits (`feat:`, `fix:`, `docs:`).
7. Open a PR.

## Code Style

- Ruff (100 char line length, py311 target).
- Type hints where helpful.
- Pydantic for request/response validation.
