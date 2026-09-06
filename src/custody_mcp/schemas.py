"""Typed inputs and structured outputs for Custody's MCP tools."""

from typing import Any, Literal

from pydantic import BaseModel, Field

EventType = Literal[
    "placed",
    "moved",
    "found",
    "checked_out",
    "checked_in",
    "marked_missing",
]
Visibility = Literal["private", "shared", "restricted"]
SearchResult = Literal["found", "not_found", "skip", "cancel"]
ToolStatus = Literal[
    "ok",
    "not_found",
    "confirmation_required",
    "forbidden",
    "completed",
]


class CustodyToolResponse(BaseModel):
    """A concise voice response plus machine-readable tool state."""

    status: ToolStatus
    speech: str = Field(description="Voice-ready response of no more than 25 words")
    item_id: str | None = None
    confirmation_required: bool = False
    next_action: str | None = None
    data: dict[str, Any] = Field(default_factory=dict)
