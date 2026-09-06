"""Integration test for the mounted Streamable HTTP transport."""

from fastapi.testclient import TestClient

from custody_mcp.app import app


def test_streamable_http_initialize() -> None:
    """An MCP client can initialize through the public /mcp route."""
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2025-11-25",
            "capabilities": {},
            "clientInfo": {"name": "custody-test", "version": "1.0"},
        },
    }
    headers = {
        "Accept": "application/json, text/event-stream",
        "Content-Type": "application/json",
    }

    with TestClient(app, base_url="http://localhost:8000") as client:
        response = client.post("/mcp", json=request, headers=headers)

    assert response.status_code == 200
    assert "mcp-server-custody" in response.text
