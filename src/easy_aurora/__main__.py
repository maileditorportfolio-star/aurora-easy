"""Package entry point."""

from __future__ import annotations

import argparse

from .config import get_settings


def main() -> None:
    parser = argparse.ArgumentParser(description="Easy Aurora RAG")
    parser.add_argument("--serve", action="store_true", help="Start the API server")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    if args.serve:
        import uvicorn

        uvicorn.run("easy_aurora.api.app:app", host=args.host, port=args.port, reload=True)
        return

    settings = get_settings()
    settings.validate()
    print("Easy Aurora RAG. Use --serve to start the API server.")


if __name__ == "__main__":
    main()
