"""Tests for Custody's registered MCP tool contracts."""

from collections.abc import Mapping
from typing import Any

import pytest
from mcp.types import CallToolResult

from custody_mcp.mcp_server import mcp
from custody_mcp.schemas import CustodyToolResponse

EXPECTED_TOOLS = {
    "record_item_event",
    "locate_item",
    "start_lost_mode",
    "continue_lost_mode",
    "set_item_access",
    "forget_item",
}

TOOL_CALLS: dict[str, dict[str, Any]] = {
    "record_item_event": {
        "item_name": "keys",
        "event_type": "placed",
        "actor_id": "user1",
        "location": "hallway console",
    },
    "locate_item": {"item_name": "keys", "requester_id": "user1"},
    "start_lost_mode": {"item_name": "keys", "requester_id": "user1"},
    "continue_lost_mode": {
        "search_session_id": "session1",
        "result": "not_found",
        "requester_id": "user1",
    },
    "set_item_access": {
        "item_name": "keys",
        "requester_id": "user1",
        "visibility": "private",
    },
    "forget_item": {
        "item_name": "keys",
        "requester_id": "user1",
        "confirmed": False,
    },
}


def _structured_response(result: CallToolResult) -> CustodyToolResponse:
    assert result.is_error is False
    assert result.structured_content is not None
    return CustodyToolResponse.model_validate(result.structured_content)


@pytest.mark.asyncio
async def test_mcp_exposes_exactly_six_typed_tools() -> None:
    """Discovery returns the final six tools, each with an output schema."""
    tools = await mcp.list_tools()

    assert {tool.name for tool in tools} == EXPECTED_TOOLS
    assert all(tool.output_schema is not None for tool in tools)

    record_tool = next(tool for tool in tools if tool.name == "record_item_event")
    assert record_tool.input_schema["properties"]["event_type"]["enum"] == [
        "placed",
        "moved",
        "found",
        "checked_out",
        "checked_in",
        "marked_missing",
    ]


@pytest.mark.asyncio
@pytest.mark.parametrize(("tool_name", "arguments"), TOOL_CALLS.items())
async def test_registered_tool_is_callable(
    tool_name: str,
    arguments: Mapping[str, Any],
) -> None:
    """Invoke every tool through MCP's real registration and conversion layer."""
    result = await mcp.call_tool(tool_name, dict(arguments))
    response = _structured_response(result)

    assert response.data["implementation"] == "stub"
    assert len(response.speech.split()) <= 25


@pytest.mark.asyncio
async def test_forget_item_requires_confirmation() -> None:
    """An unconfirmed destructive request returns a confirmation turn."""
    result = await mcp.call_tool(
        "forget_item",
        {"item_name": "keys", "requester_id": "user1", "confirmed": False},
    )
    response = _structured_response(result)

    assert response.status == "confirmation_required"
    assert response.confirmation_required is True
    assert response.next_action == "forget_item"


@pytest.mark.asyncio
async def test_forget_item_accepts_explicit_confirmation() -> None:
    """The second confirmed turn completes the scaffold flow."""
    result = await mcp.call_tool(
        "forget_item",
        {"item_name": "keys", "requester_id": "user1", "confirmed": True},
    )
    response = _structured_response(result)

    assert response.status == "completed"
    assert response.confirmation_required is False
