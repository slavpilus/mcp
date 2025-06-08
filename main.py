"""
Enneagora - FastMCP Server for E-commerce Customer Support

This server provides MCP-compliant tools for handling e-commerce customer support queries
and can be accessed by any MCP client via SSE transport.
"""

import logging
import os
from pathlib import Path

from starlette.requests import Request
from starlette.responses import HTMLResponse

from mcp.server import FastMCP
from mcp_server.mcp_tools import register_tools

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("Enneagora - E-commerce MCP Server")

# Register all e-commerce tools
tools = register_tools(mcp)


# Custom route for the root page
@mcp.custom_route("/", methods=["GET"])
async def homepage(request: Request) -> HTMLResponse:
    """Serve a static HTML page with information about the MCP server."""
    # Load HTML from file
    html_file = Path(__file__).parent / "static" / "index.html"

    try:
        html_content = html_file.read_text()
        return HTMLResponse(content=html_content)
    except FileNotFoundError:
        # Fallback if file not found
        return HTMLResponse(
            content="<h1>Enneagora - E-commerce MCP Server</h1><p>MCP endpoint: /sse</p>",
            status_code=500,
        )


if __name__ == "__main__":
    # Configure server settings for Hugging Face Spaces
    port = int(os.getenv("PORT", "7860"))  # HF Spaces default port is 7860

    # Update FastMCP settings directly
    mcp.settings.host = "0.0.0.0"
    mcp.settings.port = port

    logger.info(f"Starting Enneagora MCP Server on 0.0.0.0:{port}")
    logger.info(f"PORT env var: {os.getenv('PORT', 'not set')}")

    # Log available routes
    logger.info("Available routes:")
    logger.info(f"  - SSE endpoint: {mcp.settings.sse_path}")
    logger.info(f"  - Mount path: {mcp.settings.mount_path}")

    # Run with explicit mount path
    mcp.run(transport="sse", mount_path="/sse")
