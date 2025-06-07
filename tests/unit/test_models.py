from datetime import datetime

from mcp_server.strategies.base import (
    Address,
    Order,
    OrderEntry,
    Return,
    ShippingOption,
    TrackingInfo,
)


def test_address_model():
    """Test Address model."""
    address = Address(
        line_1="123 Main St",
        line_2="Apt 4B",
        line_3="",
        town="New York",
        postcode="10001",
        country="USA",
        phone="555-1234",
    )
    assert address.line_1 == "123 Main St"
    assert address.line_2 == "Apt 4B"
    assert address.town == "New York"
    assert address.postcode == "10001"
    assert address.country == "USA"
    assert address.phone == "555-1234"


def test_order_entry_model():
    """Test OrderEntry model."""
    entry = OrderEntry(
        entry_id="ENTRY-001",
        product_id="PROD-123",
        quantity=2,
        entry_amount=50.00,
        status="active",
    )
    assert entry.entry_id == "ENTRY-001"
    assert entry.product_id == "PROD-123"
    assert entry.quantity == 2
    assert entry.entry_amount == 50.00
    assert entry.status == "active"


def test_order_model():
    """Test Order model."""
    address = Address(
        line_1="123 Main St",
        line_2="",
        line_3="",
        town="New York",
        postcode="10001",
        country="USA",
        phone="555-1234",
    )

    entry = OrderEntry(
        entry_id="ENTRY-001",
        product_id="PROD-123",
        quantity=1,
        entry_amount=25.00,
        status="active",
    )

    order = Order(
        order_id="ORD-1000",
        customer_id="CUST-100",
        status="processing",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        entries=[entry],
        total_amount=25.00,
        shipping_address=address,
        billing_address=address,
        tracking_number="TRK123456789",
    )

    assert order.order_id == "ORD-1000"
    assert order.customer_id == "CUST-100"
    assert order.status == "processing"
    assert len(order.entries) == 1
    assert order.total_amount == 25.00
    assert order.tracking_number == "TRK123456789"


def test_return_model():
    """Test Return model."""
    ret = Return(
        return_id="RET-001",
        order_id="ORD-1000",
        status="initiated",
        reason="Damaged item",
        items=["ENTRY-001"],
        created_at=datetime.now(),
        refund_amount=25.00,
    )
    assert ret.return_id == "RET-001"
    assert ret.order_id == "ORD-1000"
    assert ret.status == "initiated"
    assert ret.reason == "Damaged item"
    assert len(ret.items) == 1
    assert ret.refund_amount == 25.00


def test_tracking_info_model():
    """Test TrackingInfo model."""
    tracking = TrackingInfo(
        tracking_number="TRK123456789",
        carrier="UPS",
        status="in_transit",
        last_update=datetime.now(),
        estimated_delivery=datetime.now(),
        current_location="Chicago, IL",
        history=[
            {
                "timestamp": datetime.now().isoformat(),
                "location": "New York",
                "status": "Package picked up",
            }
        ],
    )
    assert tracking.tracking_number == "TRK123456789"
    assert tracking.carrier == "UPS"
    assert tracking.status == "in_transit"
    assert tracking.current_location == "Chicago, IL"
    assert len(tracking.history) == 1


def test_shipping_option_model():
    """Test ShippingOption model."""
    option = ShippingOption(
        option_id="standard", name="Standard Shipping", estimated_days=5, cost=9.99
    )
    assert option.option_id == "standard"
    assert option.name == "Standard Shipping"
    assert option.estimated_days == 5
    assert option.cost == 9.99
