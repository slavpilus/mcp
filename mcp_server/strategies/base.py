"""Base strategy interface for e-commerce platforms."""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any

from pydantic import BaseModel


class Address(BaseModel):
    """Address data model."""

    line_1: str
    line_2: str
    line_3: str
    town: str
    postcode: str
    country: str
    phone: str


class OrderEntry(BaseModel):
    """Order entry data model."""

    entry_id: str
    product_id: str
    quantity: int
    entry_amount: float
    status: str


class Order(BaseModel):
    """Order data model."""

    order_id: str
    customer_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    entries: list[OrderEntry]
    total_amount: float
    shipping_address: Address
    billing_address: Address
    tracking_number: str | None = None


class Return(BaseModel):
    """Return data model."""

    return_id: str
    order_id: str
    status: str
    reason: str
    items: list[str]
    created_at: datetime
    refund_amount: float


class TrackingInfo(BaseModel):
    """Tracking information model."""

    tracking_number: str
    carrier: str
    status: str
    estimated_delivery: datetime | None = None
    current_location: str | None = None
    history: list[dict[str, Any]] = []


class ShippingOption(BaseModel):
    """Shipping option model."""

    option_id: str
    name: str
    estimated_days: int
    cost: float


class EcommerceStrategy(ABC):
    """Abstract base class for e-commerce platform strategies."""

    @abstractmethod
    async def get_order(self, order_id: str) -> Order | None:
        """Retrieve order details by order ID."""
        pass

    @abstractmethod
    async def get_customer_orders(
        self, customer_id: str, filters: dict[str, Any] | None = None
    ) -> list[Order]:
        """Get all orders for a specific customer."""
        pass

    @abstractmethod
    async def update_order_status(self, order_id: str, new_status: str) -> bool:
        """Update the status of an order."""
        pass

    @abstractmethod
    async def cancel_order(self, order_id: str, reason: str) -> bool:
        """Cancel an order with a reason."""
        pass

    @abstractmethod
    async def initiate_return(
        self, order_id: str, items: list[str], reason: str
    ) -> Return:
        """Initiate a return for specific items in an order."""
        pass

    @abstractmethod
    async def get_order_tracking(self, order_id: str) -> TrackingInfo | None:
        """Get tracking information for an order."""
        pass

    @abstractmethod
    async def search_orders(self, query_params: dict[str, Any]) -> list[Order]:
        """Search orders based on various parameters."""
        pass

    @abstractmethod
    async def get_return_policy(self) -> str:
        """Get the return policy text."""
        pass

    @abstractmethod
    async def get_shipping_options(self, order_id: str) -> list[ShippingOption]:
        """Get available shipping options for an order."""
        pass
