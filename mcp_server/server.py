"""MCP Server implementation for e-commerce support."""

import logging
from typing import Any

from .strategies.base import EcommerceStrategy
from .strategies.mock_strategy import MockDataStrategy

logger = logging.getLogger(__name__)


class MCPServer:
    """Main MCP server for handling e-commerce operations."""

    def __init__(self, strategy: EcommerceStrategy | None = None):
        """Initialize the MCP server with a strategy."""
        self.strategy = strategy or MockDataStrategy()
        self._context: dict[str, Any] = {}

    async def process_request(self, request: dict[str, Any]) -> dict[str, Any]:
        """Process incoming request and return response."""
        # Placeholder implementation
        intent = request.get("intent", "unknown")

        if intent == "get_order":
            order_id = request.get("order_id")
            if order_id:
                order = await self.strategy.get_order(order_id)
                return {"success": True, "order": order.model_dump() if order else None}

        return {"success": False, "error": "Unknown intent"}

    def update_context(self, context: dict[str, Any]) -> None:
        """Update conversation context."""
        self._context.update(context)

    def get_context(self) -> dict[str, Any]:
        """Get current conversation context."""
        return self._context.copy()
