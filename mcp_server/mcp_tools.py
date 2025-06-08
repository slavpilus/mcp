"""
MCP Tool Definitions for Enneagora E-commerce Server.

This module contains the tool function definitions that can be registered
with any FastMCP instance to avoid duplication between SSE and STDIO servers.
"""

from typing import Any

from .server import EcommerceMCPServer

# Initialize the e-commerce server instance
ecommerce_server = EcommerceMCPServer()


def register_tools(mcp_instance: Any) -> dict[str, Any]:
    """Register all e-commerce tools with the given FastMCP instance."""

    @mcp_instance.tool()
    async def get_order_status(order_id: str, customer_id: str = "default") -> str:
        """
        Get status for a specific order.

        Args:
            order_id: The order identifier (e.g., "ORD-1001")
            customer_id: Customer identifier for validation (default: "default")

        Returns:
            Formatted order status information including tracking details if shipped
        """
        return await ecommerce_server.get_order_status(order_id, customer_id)

    @mcp_instance.tool()
    async def cancel_order(
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
        return await ecommerce_server.cancel_order(order_id, reason, customer_id)

    @mcp_instance.tool()
    async def process_return(
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
        return await ecommerce_server.process_return(
            order_id, item_ids, reason, customer_id
        )

    @mcp_instance.tool()
    async def track_package(order_id: str, customer_id: str = "default") -> str:
        """
        Track package delivery status for an order.

        Args:
            order_id: The order identifier to track (e.g., "ORD-1001")
            customer_id: Customer identifier for validation (default: "default")

        Returns:
            Detailed tracking information including carrier, status, and delivery estimate
        """
        return await ecommerce_server.track_package(order_id, "order", customer_id)

    @mcp_instance.tool()
    async def get_support_info(
        topic: str = "general", customer_id: str = "default"
    ) -> str:
        """
        Get customer support information for a specific topic.

        Args:
            topic: Support topic - "returns", "shipping", "contact", or "general" (default: "general")
            customer_id: Customer identifier (default: "default")

        Returns:
            Relevant support information based on the topic
        """
        return await ecommerce_server.get_support_info(topic, customer_id)

    return {
        "get_order_status": get_order_status,
        "cancel_order": cancel_order,
        "process_return": process_return,
        "track_package": track_package,
        "get_support_info": get_support_info,
    }
