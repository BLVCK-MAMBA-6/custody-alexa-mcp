"""The six-tool MCP surface for Custody."""

from datetime import datetime

from mcp.server import MCPServer

from .schemas import CustodyToolResponse, EventType, SearchResult, Visibility

mcp = MCPServer(
    "mcp-server-custody",
    instructions=(
        "Use Custody to remember and locate physical items, track shared-item "
        "custody, correct stale locations, and guide Lost Mode. Treat every "
        "location as last reported rather than physically verified. Speak only "
        "the response's speech field to the user."
    ),
)


def _stub_data(**values: object) -> dict[str, object]:
    """Mark scaffold output so no caller mistakes it for persisted state."""
    return {"implementation": "stub", **values}


@mcp.tool(title="Record an item event")
async def record_item_event(
    item_name: str,
    event_type: EventType,
    actor_id: str,
    location: str | None = None,
    holder_id: str | None = None,
    occurred_at: datetime | None = None,
    operation_id: str | None = None,
) -> CustodyToolResponse:
    """Record that an item was placed, moved, found, borrowed, returned, or missing."""
    return CustodyToolResponse(
        status="ok",
        speech="Item event received. Persistent storage is not connected yet.",
        data=_stub_data(
            item_name=item_name,
            event_type=event_type,
            actor_id=actor_id,
            location=location,
            holder_id=holder_id,
            occurred_at=occurred_at.isoformat() if occurred_at else None,
            operation_id=operation_id,
        ),
    )


@mcp.tool(title="Locate an item")
async def locate_item(item_name: str, requester_id: str) -> CustodyToolResponse:
    """Return an authorized item's last reported location or current holder."""
    return CustodyToolResponse(
        status="not_found",
        speech="I don't have a saved location for that item yet.",
        data=_stub_data(item_name=item_name, requester_id=requester_id),
    )


@mcp.tool(title="Start Lost Mode")
async def start_lost_mode(item_name: str, requester_id: str) -> CustodyToolResponse:
    """Start a guided search and return only the first place to check."""
    return CustodyToolResponse(
        status="not_found",
        speech="I don't have enough location history to start Lost Mode yet.",
        data=_stub_data(item_name=item_name, requester_id=requester_id),
    )


@mcp.tool(title="Continue Lost Mode")
async def continue_lost_mode(
    search_session_id: str,
    result: SearchResult,
    requester_id: str,
    found_location: str | None = None,
) -> CustodyToolResponse:
    """Record a search result and return the next step or finish the search."""
    return CustodyToolResponse(
        status="ok",
        speech="Search update received. Search history is not connected yet.",
        data=_stub_data(
            search_session_id=search_session_id,
            result=result,
            requester_id=requester_id,
            found_location=found_location,
        ),
    )


@mcp.tool(title="Set item access")
async def set_item_access(
    item_name: str,
    requester_id: str,
    visibility: Visibility,
    allowed_user_ids: list[str] | None = None,
) -> CustodyToolResponse:
    """Set an owned item as private, household-shared, or restricted."""
    return CustodyToolResponse(
        status="ok",
        speech="Access preference received. Persistent storage is not connected yet.",
        data=_stub_data(
            item_name=item_name,
            requester_id=requester_id,
            visibility=visibility,
            allowed_user_ids=allowed_user_ids or [],
        ),
    )


@mcp.tool(title="Forget an item")
async def forget_item(
    item_name: str,
    requester_id: str,
    confirmed: bool = False,
) -> CustodyToolResponse:
    """Permanently delete an owned item's records after explicit confirmation."""
    if not confirmed:
        return CustodyToolResponse(
            status="confirmation_required",
            speech="Permanently delete this item's history? Say yes to confirm.",
            confirmation_required=True,
            next_action="forget_item",
            data=_stub_data(item_name=item_name, requester_id=requester_id),
        )

    return CustodyToolResponse(
        status="completed",
        speech="Confirmation received. Persistent storage is not connected yet.",
        data=_stub_data(item_name=item_name, requester_id=requester_id, confirmed=True),
    )
