"""API response envelope matching the ecommerce1 standard: { success, data | message, details }."""

from __future__ import annotations

from typing import Any


def ok(data: Any = None, message: str | None = None) -> dict[str, Any]:
    return {"success": True, "data": data, "message": message, "details": None}


def fail(message: str, details: Any = None) -> dict[str, Any]:
    return {"success": False, "data": None, "message": message, "details": details}
