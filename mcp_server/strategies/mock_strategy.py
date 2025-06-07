"""Mock data strategy for testing and development."""

import random
from datetime import datetime, timedelta
from typing import Any

from faker import Faker

from .base import (
    Address,
    EcommerceStrategy,
    Order,
    OrderEntry,
    Return,
    ShippingOption,
    TrackingInfo,
)

fake = Faker()


class MockDataStrategy(EcommerceStrategy):
    """Mock implementation of e-commerce strategy for testing."""

    def __init__(self) -> None:
        """Initialize mock data strategy with sample data."""
        self.orders: dict[str, Order] = {}
        self.returns: dict[str, Return] = {}
        self._generate_mock_data()

    def _generate_mock_data(self) -> None:
        """Generate sample orders for testing."""
        # Generate 20 sample orders
        for i in range(20):
            order_id = f"ORD-{1000 + i}"
            customer_id = f"CUST-{random.randint(100, 200)}"

            # Create order with various statuses
            statuses = ["pending", "processing", "shipped", "delivered", "cancelled"]
            status = random.choice(statuses)

            created_at = datetime.now() - timedelta(days=random.randint(1, 30))

            # Generate order entries
            num_entries = random.randint(1, 4)
            entries = []
            total = 0.0

            for j in range(num_entries):
                quantity = random.randint(1, 3)
                price_per_item = round(random.uniform(10, 200), 2)
                entry_amount = round(quantity * price_per_item, 2)
                total += entry_amount

                entry = OrderEntry(
                    entry_id=f"ENTRY-{order_id}-{j + 1}",
                    product_id=f"PROD-{random.randint(1, 100)}",
                    quantity=quantity,
                    entry_amount=entry_amount,
                    status="active" if status not in ["cancelled"] else "cancelled",
                )
                entries.append(entry)

            # Create shipping address
            shipping_address = Address(
                line_1=fake.street_address(),
                line_2=fake.secondary_address() if random.random() > 0.7 else "",
                line_3="",
                town=fake.city(),
                postcode=fake.zipcode(),
                country="USA",
                phone=fake.phone_number(),
            )

            # Create billing address (sometimes same as shipping)
            if random.random() > 0.3:  # 70% chance billing is same as shipping
                billing_address = shipping_address
            else:
                billing_address = Address(
                    line_1=fake.street_address(),
                    line_2=fake.secondary_address() if random.random() > 0.7 else "",
                    line_3="",
                    town=fake.city(),
                    postcode=fake.zipcode(),
                    country="USA",
                    phone=fake.phone_number(),
                )

            order = Order(
                order_id=order_id,
                customer_id=customer_id,
                status=status,
                created_at=created_at,
                updated_at=created_at + timedelta(hours=random.randint(1, 48)),
                entries=entries,
                total_amount=total,
                shipping_address=shipping_address,
                billing_address=billing_address,
                tracking_number=(
                    f"TRK{fake.numerify('############')}"
                    if status in ["shipped", "delivered"]
                    else None
                ),
            )

            self.orders[order_id] = order

    async def get_order(self, order_id: str) -> Order | None:
        """Retrieve order details by order ID."""
        return self.orders.get(order_id)

    async def get_customer_orders(
        self, customer_id: str, filters: dict[str, Any] | None = None
    ) -> list[Order]:
        """Get all orders for a specific customer."""
        customer_orders = [
            order for order in self.orders.values() if order.customer_id == customer_id
        ]

        # Apply filters if provided
        if filters:
            if "status" in filters:
                customer_orders = [
                    order
                    for order in customer_orders
                    if order.status == filters["status"]
                ]
            if "date_from" in filters:
                customer_orders = [
                    order
                    for order in customer_orders
                    if order.created_at >= filters["date_from"]
                ]

        return sorted(customer_orders, key=lambda x: x.created_at, reverse=True)

    async def update_order_status(self, order_id: str, new_status: str) -> bool:
        """Update the status of an order."""
        if order_id in self.orders:
            self.orders[order_id].status = new_status
            self.orders[order_id].updated_at = datetime.now()
            return True
        return False

    async def cancel_order(self, order_id: str, reason: str) -> bool:
        """Cancel an order with a reason."""
        if order_id in self.orders and self.orders[order_id].status in [
            "pending",
            "processing",
        ]:
            self.orders[order_id].status = "cancelled"
            self.orders[order_id].updated_at = datetime.now()
            return True
        return False

    async def initiate_return(
        self, order_id: str, items: list[str], reason: str
    ) -> Return:
        """Initiate a return for specific items in an order."""
        return_id = f"RET-{fake.numerify('####')}"

        return_obj = Return(
            return_id=return_id,
            order_id=order_id,
            status="initiated",
            reason=reason,
            items=items,
            created_at=datetime.now(),
            refund_amount=round(random.uniform(10, 500), 2),
        )

        self.returns[return_id] = return_obj
        return return_obj

    async def get_order_tracking(self, order_id: str) -> TrackingInfo | None:
        """Get tracking information for an order."""
        order = self.orders.get(order_id)
        if not order or not order.tracking_number:
            return None

        carrier = random.choice(["UPS", "FedEx", "USPS", "DHL"])

        return TrackingInfo(
            tracking_number=order.tracking_number,
            carrier=carrier,
            status=order.status,
            last_update=datetime.now() - timedelta(hours=random.randint(1, 24)),
            estimated_delivery=order.created_at + timedelta(days=random.randint(3, 7)),
            tracking_url=f"https://{carrier.lower()}.com/track/{order.tracking_number}",
            current_location=fake.city() + ", " + fake.state_abbr(),
            history=[
                {
                    "timestamp": order.created_at + timedelta(hours=i * 12),
                    "location": fake.city() + ", " + fake.state_abbr(),
                    "status": f"Package {random.choice(['scanned', 'in transit', 'out for delivery'])}",
                }
                for i in range(random.randint(2, 5))
            ],
        )

    async def search_orders(self, query_params: dict[str, Any]) -> list[Order]:
        """Search orders based on various parameters."""
        results = list(self.orders.values())

        # Filter by search criteria
        if "order_id" in query_params:
            results = [o for o in results if query_params["order_id"] in o.order_id]

        if "customer_id" in query_params:
            results = [
                o for o in results if o.customer_id == query_params["customer_id"]
            ]

        if "status" in query_params:
            results = [o for o in results if o.status == query_params["status"]]

        return results

    async def get_return_policy(self) -> str:
        """Get the return policy text."""
        return """
        **Return Policy**

        We offer a 30-day return policy on all items. To be eligible for a return:
        - Items must be unused and in original packaging
        - Receipt or proof of purchase is required
        - Some items may be subject to restocking fees

        To initiate a return, contact our customer service team with your order number.
        """

    async def get_shipping_options(self, order_id: str) -> list[ShippingOption]:
        """Get available shipping options for an order."""
        return [
            ShippingOption(
                option_id="standard",
                name="Standard Shipping",
                estimated_days=5,
                cost=9.99,
            ),
            ShippingOption(
                option_id="express",
                name="Express Shipping",
                estimated_days=2,
                cost=19.99,
            ),
            ShippingOption(
                option_id="overnight",
                name="Overnight Shipping",
                estimated_days=1,
                cost=39.99,
            ),
        ]
