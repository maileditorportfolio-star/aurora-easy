"""Tests for API endpoints."""

from fastapi.testclient import TestClient

from easy_aurora.api.app import app


def test_health():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
    assert body["data"]["status"] == "ok"


def test_query_empty():
    client = TestClient(app)
    resp = client.post("/query", json={"question": ""})
    assert resp.status_code == 400
