import logging
from typing import Any

from .strategies.base import EcommerceStrategy
from .strategies.mock_strategy import MockDataStrategy

logger = logging.getLogger(__name__)


class EcommerceMCPServer:
    """Enneagora - MCP Server for E-commerce Customer Support Tools."""

    def __init__(self, ecommerce_strategy: EcommerceStrategy | None = None):
        """Initialize MCP server with e-commerce strategy."""
        self.ecommerce_strategy = ecommerce_strategy or MockDataStrategy()
        logger.info("Enneagora MCP Server initialized with e-commerce strategy")

    def get_order_status(self, order_id: str, customer_id: str = "default") -> str:
        """
        Get status for a specific order.

        Args:
            order_id: The order identifier (e.g., "ORD-1001")
            customer_id: Customer identifier for validation

        Returns:
            Formatted order status information
        """
        try:
            # Get order details
            order = self._run_sync(self.ecommerce_strategy.get_order(order_id))
            if not order:
                return f"Order {order_id} not found. Please check the order number and try again."

            # Format response
            response = f"Order {order.order_id} Status: {order.status.title()}\n"
            response += f"Order Date: {order.created_at.strftime('%B %d, %Y')}\n"
            response += f"Total: ${order.total_amount:.2f}\n"

            if order.status == "shipped":
                tracking = self._run_sync(
                    self.ecommerce_strategy.get_order_tracking(order_id)
                )
                if tracking:
                    response += f"\nTracking Number: {tracking.tracking_number}\n"
                    response += f"Carrier: {tracking.carrier}\n"
                    response += f"Current Status: {tracking.status}\n"
                    if tracking.estimated_delivery:
                        response += f"Estimated Delivery: {tracking.estimated_delivery.strftime('%B %d, %Y')}"

            return response

        except Exception as e:
            logger.error(f"Error in get_order_status: {e}")
            return "I encountered an error while checking your order status. Please try again later."

    def cancel_order(
        self,
        order_id: str,
        reason: str = "Customer requested",
        customer_id: str = "default",
    ) -> str:
        """
        Cancel an order.

        Args:
            order_id: The order identifier to cancel
            reason: Reason for cancellation
            customer_id: Customer identifier for validation

        Returns:
            Cancellation confirmation or error message
        """
        try:
            # Get order details
            order = self._run_sync(self.ecommerce_strategy.get_order(order_id))
            if not order:
                return f"Order {order_id} not found. Please check the order number and try again."

            # Check if cancellation is possible
            if order.status in ["delivered", "cancelled"]:
                return f"Order {order_id} cannot be cancelled as it is already {order.status}."

            if order.status == "shipped":
                return f"Order {order_id} has already shipped. Please use our return process instead."

            # Attempt cancellation
            success = self._run_sync(
                self.ecommerce_strategy.cancel_order(order_id, reason)
            )

            if success:
                return f"Order {order_id} has been successfully cancelled. You will receive a confirmation email shortly, and any charges will be refunded within 3-5 business days."
            else:
                return f"Unable to cancel order {order_id}. Please contact customer service for assistance."

        except Exception as e:
            logger.error(f"Error in cancel_order: {e}")
            return "I encountered an error while processing your cancellation. Please try again later."

    def process_return(
        self,
        order_id: str,
        item_ids: list[str] | None = None,
        reason: str = "Customer return",
        customer_id: str = "default",
    ) -> str:
        """
        Process a return request.

        Args:
            order_id: The order identifier to return
            item_ids: List of specific item IDs to return (None = all items)
            reason: Reason for return
            customer_id: Customer identifier for validation

        Returns:
            Return instructions and confirmation
        """
        try:
            # Get order details
            order = self._run_sync(self.ecommerce_strategy.get_order(order_id))
            if not order:
                return f"Order {order_id} not found. Please check the order number and try again."

            # Check return eligibility
            if order.status not in ["delivered", "shipped"]:
                return f"Order {order_id} is currently {order.status} and cannot be returned yet. Returns are available after delivery."

            # If no specific items specified, return all items
            if not item_ids:
                item_ids = [entry.product_id for entry in order.entries]

            # Process return
            return_info = self._run_sync(
                self.ecommerce_strategy.initiate_return(order_id, item_ids, reason)
            )

            if return_info:
                response = f"Return initiated for order {order_id}\n"
                response += f"Return ID: {return_info.return_id}\n"
                response += f"Items: {', '.join(item_ids)}\n\n"
                response += "Next Steps:\n"
                response += "1. A prepaid return label has been emailed to you\n"
                response += "2. Package the items in original packaging if possible\n"
                response += (
                    "3. Attach the return label and drop off at any shipping location\n"
                )
                response += (
                    "4. Refund will be processed within 5-7 business days after receipt"
                )
                return response
            else:
                return f"Unable to process return for order {order_id}. Please contact customer service for assistance."

        except Exception as e:
            logger.error(f"Error in process_return: {e}")
            return "I encountered an error while processing your return. Please try again later."

    def track_package(
        self,
        identifier: str,
        identifier_type: str = "order",
        customer_id: str = "default",
    ) -> str:
        """
        Track a package by order ID or tracking number.

        Args:
            identifier: Order ID or tracking number
            identifier_type: Type of identifier - "order" or "tracking"
            customer_id: Customer identifier for validation

        Returns:
            Detailed tracking information
        """
        try:
            # Get tracking information
            if identifier_type == "order":
                tracking = self._run_sync(
                    self.ecommerce_strategy.get_order_tracking(identifier)
                )
                if not tracking:
                    return f"No tracking information found for order {identifier}."
            else:
                # For tracking numbers, we'd need a separate method in real implementation
                # For now, return an error
                return "Tracking by tracking number not yet implemented. Please provide an order ID instead."

            # Format tracking response
            response = f"Package Tracking: {tracking.tracking_number}\n"
            response += f"Carrier: {tracking.carrier}\n"
            response += f"Current Status: {tracking.status}\n"
            response += f"Last Update: {tracking.last_update.strftime('%B %d, %Y at %I:%M %p')}\n"

            if tracking.estimated_delivery:
                response += f"Estimated Delivery: {tracking.estimated_delivery.strftime('%B %d, %Y')}\n"

            if tracking.tracking_url:
                response += f"\nFor detailed tracking, visit: {tracking.tracking_url}"

            return response

        except Exception as e:
            logger.error(f"Error in track_package: {e}")
            return "I encountered an error while tracking your package. Please try again later."

    def get_support_info(
        self, topic: str = "general", customer_id: str = "default"
    ) -> str:
        """
        Get support information for a specific topic.

        Args:
            topic: Support topic - "returns", "shipping", "contact", or "general"
            customer_id: Customer identifier

        Returns:
            Relevant support information
        """
        try:
            topic_lower = topic.lower()

            if "return" in topic_lower or "refund" in topic_lower:
                policy_info = self._run_sync(
                    self.ecommerce_strategy.get_return_policy()
                )
                return f"Return Policy:\n{policy_info}\n\nTo process a return, provide your order number."

            elif "shipping" in topic_lower or "delivery" in topic_lower:
                return """Shipping Information:
• Standard shipping: 5-7 business days ($5.99)
• Express shipping: 2-3 business days ($12.99)
• Overnight shipping: 1 business day ($24.99)

Free standard shipping on orders over $50!"""

            elif "contact" in topic_lower or "support" in topic_lower:
                return """Contact Information:
• Phone: 1-800-SUPPORT (24/7)
• Email: support@example.com
• Live Chat: Available on our website

We're here to help with orders, returns, and any questions!"""

            else:
                return """How can I help you today? I can assist with:
• Order status and tracking
• Order cancellations
• Returns and refunds
• Shipping information
• Contact information

Please let me know what you need help with!"""

        except Exception as e:
            logger.error(f"Error in get_support_info: {e}")
            return "I encountered an error. Please contact customer support at 1-800-SUPPORT."

    def _run_sync(self, coro: Any) -> Any:
        """Run async coroutine synchronously."""
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()
