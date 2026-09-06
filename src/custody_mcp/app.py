"""FastAPI host for Custody's Streamable HTTP MCP application."""

import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from .config import settings
from .mcp_server import mcp

logging.basicConfig(level=settings.log_level)
logger = logging.getLogger(__name__)

# The SDK creates ``session_manager`` lazily inside this call.
mcp_http_app = mcp.streamable_http_app()


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Run the MCP session manager for the lifetime of the FastAPI host."""
    logger.info("Starting mcp-server-custody")
    async with mcp.session_manager.run():
        yield
    logger.info("Stopped mcp-server-custody")


app = FastAPI(
    title="Custody MCP Server",
    description="Voice-first shared object memory for Alexa+",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health", tags=["operations"])
async def health() -> dict[str, str]:
    """Return a dependency-free liveness response."""
    return {"status": "ok", "service": "mcp-server-custody"}


# Mount last: Mount("/") matches every path and would hide later FastAPI routes.
app.mount("/", mcp_http_app)


def main() -> None:
    """Run Custody with its configured host and port."""
    import uvicorn

    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    main()
