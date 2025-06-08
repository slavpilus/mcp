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

    def _parse_order_id(self, order_id: str) -> tuple[str, bool]:
        """
        Parse order ID to determine status and existence.

        Returns:
            tuple: (status, should_exist)
        """
        # Handle error/not found cases
        if order_id.endswith("-E") or order_id.upper() == "ORD-ERROR":
            return "error", False

        # Map suffixes to statuses
        status_map = {
            "-D": "delivered",
            "-C": "cancelled",
            "-S": "shipped",
            "-P": "processing",
            "-F": "failed",
            "-R": "ready_for_pickup",
            "-T": "in_transit",
        }

        for suffix, status in status_map.items():
            if order_id.endswith(suffix):
                return status, True

        # Default to pending for orders without suffix
        return "pending", True

    def _create_dynamic_order(self, order_id: str, status: str) -> Order:
        """Create a dynamic order with specified status."""
        import random
        from datetime import datetime, timedelta

        # Extract base number from order ID for deterministic data
        base_num = "".join(filter(str.isdigit, order_id))

        # Create a local Random instance to avoid affecting global state
        local_random = random.Random()
        if base_num:
            local_random.seed(int(base_num))

        # Create deterministic customer ID
        customer_id = f"CUST-{local_random.randint(100, 999)}"

        # Create order entries
        num_entries = local_random.randint(1, 3)
        entries = []
        total = 0.0

        products = [
            ("Wireless Headphones", 99.99),
            ("Smartphone Case", 24.99),
            ("USB Cable", 12.99),
            ("Bluetooth Speaker", 79.99),
            ("Phone Charger", 19.99),
            ("Screen Protector", 9.99),
            ("Memory Card", 34.99),
            ("Tablet Stand", 29.99),
        ]

        for i in range(num_entries):
            _, price = local_random.choice(products)
            quantity = local_random.randint(1, 2)
            entry_total = price * quantity
            total += entry_total

            entries.append(
                OrderEntry(
                    entry_id=f"ENTRY-{order_id}-{i + 1}",
                    product_id=f"PROD-{local_random.randint(1000, 9999)}",
                    quantity=quantity,
                    entry_amount=entry_total,
                    status="active" if status not in ["cancelled"] else "cancelled",
                )
            )

        # Create addresses
        shipping_address = Address(
            line_1=fake.street_address(),
            line_2="",
            line_3="",
            town=fake.city(),
            postcode=fake.zipcode(),
            country="USA",
            phone=fake.phone_number(),
        )

        # Set realistic dates based on status
        now = datetime.now()
        if status == "delivered":
            created_at = now - timedelta(days=local_random.randint(7, 30))
            updated_at = now - timedelta(days=local_random.randint(1, 5))
        elif status == "shipped":
            created_at = now - timedelta(days=local_random.randint(3, 10))
            updated_at = now - timedelta(days=local_random.randint(1, 3))
        elif status == "cancelled":
            created_at = now - timedelta(days=local_random.randint(1, 14))
            updated_at = now - timedelta(days=local_random.randint(0, 2))
        else:
            created_at = now - timedelta(days=local_random.randint(0, 7))
            updated_at = created_at + timedelta(hours=local_random.randint(1, 48))

        # Generate tracking number for shipped/delivered orders
        tracking_number = None
        if status in ["shipped", "delivered", "in_transit"]:
            tracking_number = f"TRK{local_random.randint(100000000000, 999999999999)}"

        order = Order(
            order_id=order_id,
            customer_id=customer_id,
            status=status,
            created_at=created_at,
            updated_at=updated_at,
            entries=entries,
            total_amount=total,
            shipping_address=shipping_address,
            billing_address=shipping_address,  # Same as shipping for simplicity
            tracking_number=tracking_number,
        )

        # Cache the dynamically created order
        self.orders[order_id] = order
        return order

    async def get_order(self, order_id: str) -> Order | None:
        """
        Retrieve order details by order ID.

        Supports dynamic order creation based on order ID patterns:
        - ORD-XXXX-D: Delivered order
        - ORD-XXXX-C: Cancelled order
        - ORD-XXXX-S: Shipped order
        - ORD-XXXX-P: Processing order
        - ORD-XXXX-E: Error/not found
        - ORD-XXXX-F: Failed/problem order
        - ORD-XXXX-R: Ready for pickup
        - ORD-XXXX-T: In transit
        - ORD-XXXX (no suffix): Random existing order or new pending order
        """
        # Check if order exists in static data
        if order_id in self.orders:
            return self.orders[order_id]

        # Parse dynamic order ID pattern
        order_status, should_exist = self._parse_order_id(order_id)

        if not should_exist:
            return None

        # Create dynamic order based on pattern
        return self._create_dynamic_order(order_id, order_status)

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
        """
        Cancel an order with a reason.

        Dynamic behavior based on order ID:
        - ORD-XXXX-F: Always fails (simulates payment issues, etc.)
        - ORD-XXXX-C: Already cancelled
        - ORD-XXXX-D: Already delivered (cannot cancel)
        - ORD-XXXX-S: Already shipped (cannot cancel)
        """
        # Get or create the order
        order = await self.get_order(order_id)
        if not order:
            return False

        # Handle special cases based on order ID
        if order_id.endswith("-F"):
            # Simulate cancellation failure
            return False

        # Check if order can be cancelled based on status
        if order.status in ["pending", "processing"]:
            order.status = "cancelled"
            order.updated_at = datetime.now()
            return True

        # Already cancelled, delivered, or shipped orders cannot be cancelled
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
        """
        Get tracking information for an order.

        Dynamic behavior based on order ID:
        - ORD-XXXX-E: Returns None (tracking not found)
        - ORD-XXXX-F: Returns tracking with "lost" status
        - ORD-XXXX-D: Delivered with full tracking history
        - ORD-XXXX-S: Shipped and in transit
        - ORD-XXXX-T: In transit with live updates
        """
        order = await self.get_order(order_id)
        if not order:
            return None

        # Handle error cases
        if order_id.endswith("-E"):
            return None

        # Ensure tracking number exists for trackable orders
        if not order.tracking_number and order.status in [
            "shipped",
            "delivered",
            "in_transit",
            "failed",
        ]:
            order.tracking_number = f"TRK{random.randint(100000000000, 999999999999)}"

        if not order.tracking_number:
            return None

        # Determine carrier based on order ID for consistency
        carriers = ["UPS", "FedEx", "USPS", "DHL"]
        carrier_index = sum(ord(c) for c in order_id) % len(carriers)
        carrier = carriers[carrier_index]

        # Handle failed/lost packages
        if order_id.endswith("-F"):
            return TrackingInfo(
                tracking_number=order.tracking_number,
                carrier=carrier,
                status="lost",
                last_update=datetime.now() - timedelta(days=random.randint(3, 7)),
                estimated_delivery=None,
                tracking_url=f"https://{carrier.lower()}.com/track/{order.tracking_number}",
                current_location="Unknown",
                history=[
                    {
                        "timestamp": order.created_at + timedelta(hours=12),
                        "location": "Distribution Center",
                        "status": "Package scanned",
                    },
                    {
                        "timestamp": order.created_at + timedelta(days=2),
                        "location": "In Transit",
                        "status": "Package lost during transit",
                    },
                ],
            )

        # Normal tracking based on order status
        tracking_status = order.status
        if order.status == "in_transit":
            tracking_status = "in_transit"
        elif order.status == "delivered":
            tracking_status = "delivered"
        elif order.status == "shipped":
            tracking_status = "out_for_delivery"

        return TrackingInfo(
            tracking_number=order.tracking_number,
            carrier=carrier,
            status=tracking_status,
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
