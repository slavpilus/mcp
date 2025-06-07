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
from mcp_server.server import EcommerceMCPServer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the e-commerce MCP server
ecommerce_server = EcommerceMCPServer()

# Create FastMCP server instance
mcp = FastMCP("Enneagora - E-commerce MCP Server")


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


@mcp.tool()
def get_order_status(order_id: str, customer_id: str = "default") -> str:
    """
    Get status for a specific order.

    Args:
        order_id: The order identifier (e.g., "ORD-1001")
        customer_id: Customer identifier for validation (default: "default")

    Returns:
        Formatted order status information including tracking details if shipped
    """
    return ecommerce_server.get_order_status(order_id, customer_id)


@mcp.tool()
def cancel_order(
    order_id: str, reason: str = "Customer requested", customer_id: str = "default"
) -> str:
    """
    Cancel an order.

    Args:
        order_id: The order identifier to cancel (e.g., "ORD-1001")
        reason: Reason for cancellation (default: "Customer requested")
        customer_id: Customer identifier for validation (default: "default")

    Returns:
        Cancellation confirmation or error message
    """
    return ecommerce_server.cancel_order(order_id, reason, customer_id)


@mcp.tool()
def process_return(
    order_id: str,
    item_ids: list[str] | None = None,
    reason: str = "Customer return",
    customer_id: str = "default",
) -> str:
    """
    Process a return request for an order.

    Args:
        order_id: The order identifier to return (e.g., "ORD-1001")
        item_ids: List of specific item IDs to return (None = all items)
        reason: Reason for return (default: "Customer return")
        customer_id: Customer identifier for validation (default: "default")

    Returns:
        Return instructions and confirmation with return ID
    """
    return ecommerce_server.process_return(order_id, item_ids, reason, customer_id)


@mcp.tool()
def track_package(order_id: str, customer_id: str = "default") -> str:
    """
    Track package delivery status for an order.

    Args:
        order_id: The order identifier to track (e.g., "ORD-1001")
        customer_id: Customer identifier for validation (default: "default")

    Returns:
        Detailed tracking information including carrier, status, and delivery estimate
    """
    return ecommerce_server.track_package(order_id, "order", customer_id)


@mcp.tool()
def get_support_info(topic: str = "general", customer_id: str = "default") -> str:
    """
    Get customer support information for a specific topic.

    Args:
        topic: Support topic - "returns", "shipping", "contact", or "general" (default: "general")
        customer_id: Customer identifier (default: "default")

    Returns:
        Relevant support information based on the topic
    """
    return ecommerce_server.get_support_info(topic, customer_id)


if __name__ == "__main__":
    # Get port from environment (Hugging Face Spaces sets this)
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"Starting Enneagora MCP Server on {host}:{port}")
    mcp.run(transport="sse", host=host, port=port)
