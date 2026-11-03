"""API response envelope matching the ecommerce1 standard: { success, data | message, details }."""

from __future__ import annotations

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    message: str | None = None
    details: Any | None = None


def ok(data: Any = None, message: str | None = None) -> dict[str, Any]:
    return {"success": True, "data": data, "message": message, "details": None}


def fail(message: str, details: Any = None) -> dict[str, Any]:
    return {"success": False, "data": None, "message": message, "details": details}
