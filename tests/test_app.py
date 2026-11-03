"""Tests for API app endpoints."""

from fastapi.testclient import TestClient

from easy_aurora.api.app import app


def test_health_envelope():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert set(body.keys()) == {"success", "data", "message", "details"}
    assert body["success"] is True


def test_query_empty_returns_400():
    client = TestClient(app)
    resp = client.post("/query", json={"question": ""})
    assert resp.status_code == 400


def test_clear_documents():
    client = TestClient(app)
    resp = client.delete("/documents")
    assert resp.status_code == 200
    body = resp.json()
    assert body["success"] is True
