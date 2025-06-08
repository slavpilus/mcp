"""
Enneagora - FastMCP Server for E-commerce Customer Support (STDIO version)

This server provides MCP-compliant tools for handling e-commerce customer support queries
and can be accessed via stdio transport for Claude Desktop.
"""

import logging

from mcp.server import FastMCP
from mcp_server.mcp_tools import register_tools

# Configure logging to stderr so it doesn't interfere with stdio
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)

# Create FastMCP server instance
mcp = FastMCP("Enneagora - E-commerce MCP Server")

# Register all e-commerce tools
tools = register_tools(mcp)


if __name__ == "__main__":
    # Run with stdio transport for Claude Desktop
    logger.info("Starting Enneagora MCP Server in STDIO mode for Claude Desktop")
    mcp.run(transport="stdio")
