"""Tests for the FastAPI host."""

from fastapi.testclient import TestClient

from custody_mcp.app import app


def test_health_endpoint_identifies_service() -> None:
    """GET /health stays outside MCP and identifies the service."""
    response = TestClient(app).get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ok",
        "service": "mcp-server-custody",
    }
