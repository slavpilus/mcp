from datetime import datetime
from unittest.mock import patch

import pytest

from mcp_server.server import EcommerceMCPServer
from mcp_server.strategies.base import Address, Order, OrderEntry, TrackingInfo
from mcp_server.strategies.mock_strategy import MockDataStrategy


def test_server_initialization():
    """Test EcommerceMCPServer initialization."""
    # With default strategy
    server = EcommerceMCPServer()
    assert isinstance(server.ecommerce_strategy, MockDataStrategy)

    # With custom strategy
    custom_strategy = MockDataStrategy()
    server = EcommerceMCPServer(ecommerce_strategy=custom_strategy)
    assert server.ecommerce_strategy is custom_strategy


@pytest.mark.asyncio
async def test_get_order_status():
    """Test get_order_status with structured parameters."""
    server = EcommerceMCPServer()

    # Test with valid order ID
    response = await server.get_order_status("ORD-1001")
    assert "ORD-1001" in response
    assert "Status:" in response
    assert "Order Date:" in response
    assert "Total: $" in response

    # Test with invalid order ID
    response = await server.get_order_status("INVALID-ID")
    assert "not found" in response


@pytest.mark.asyncio
async def test_cancel_order():
    """Test cancel_order with structured parameters."""
    server = EcommerceMCPServer()

    # Test with valid order ID (should work if status is pending/processing)
    response = await server.cancel_order("ORD-1004", "Customer changed mind")
    # Response depends on order status in mock data
    assert "ORD-1004" in response

    # Test with invalid order ID
    response = await server.cancel_order("INVALID-ID")
    assert "not found" in response


@pytest.mark.asyncio
async def test_process_return():
    """Test process_return with structured parameters."""
    server = EcommerceMCPServer()

    # Find a delivered order from mock data
    delivered_order_id = None
    for order_id, order in server.ecommerce_strategy.orders.items():
        if order.status == "delivered":
            delivered_order_id = order_id
            break

    if delivered_order_id:
        # Test return for delivered order
        response = await server.process_return(delivered_order_id)
        assert "Return initiated" in response or "cannot be returned" in response

    # Test with invalid order ID
    response = await server.process_return("INVALID-ID")
    assert "not found" in response


@pytest.mark.asyncio
async def test_track_package():
    """Test track_package with structured parameters."""
    server = EcommerceMCPServer()

    # Find a shipped order from mock data
    shipped_order_id = None
    for order_id, order in server.ecommerce_strategy.orders.items():
        if order.status == "shipped":
            shipped_order_id = order_id
            break

    if shipped_order_id:
        # Test tracking for shipped order
        response = await server.track_package(shipped_order_id)
        assert "Package Tracking:" in response or "No tracking information" in response

    # Test with invalid order ID
    response = await server.track_package("INVALID-ID", "order")
    assert "No tracking information" in response


@pytest.mark.asyncio
async def test_get_support_info():
    """Test get_support_info with structured parameters."""
    server = EcommerceMCPServer()

    # Test general support info
    response = await server.get_support_info("general")
    assert "How can I help you" in response

    # Test returns topic
    response = await server.get_support_info("returns")
    assert "Return Policy" in response

    # Test shipping topic
    response = await server.get_support_info("shipping")
    assert "Shipping Information" in response

    # Test contact topic
    response = await server.get_support_info("contact")
    assert "Contact Information" in response


@pytest.mark.asyncio
async def test_get_order_status_with_shipped_order():
    """Test get_order_status with a shipped order that has tracking."""
    server = EcommerceMCPServer()

    # Create a mock shipped order
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
    shipped_order = Order(
        order_id="ORD-SHIPPED",
        customer_id="CUST-100",
        status="shipped",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        entries=[entry],
        total_amount=25.00,
        shipping_address=address,
        billing_address=address,
        tracking_number="TRK123456789",
    )

    # Create tracking info
    tracking_info = TrackingInfo(
        tracking_number="TRK123456789",
        carrier="UPS",
        status="in_transit",
        last_update=datetime.now(),
        estimated_delivery=datetime.now(),
        current_location="Chicago, IL",
    )

    # Mock the strategy methods
    with (
        patch.object(server.ecommerce_strategy, "get_order") as mock_get_order,
        patch.object(
            server.ecommerce_strategy, "get_order_tracking"
        ) as mock_get_tracking,
    ):

        mock_get_order.return_value = shipped_order
        mock_get_tracking.return_value = tracking_info

        response = await server.get_order_status("ORD-SHIPPED")

        assert "ORD-SHIPPED" in response
        assert "Shipped" in response
        assert "Tracking Number: TRK123456789" in response
        assert "Carrier: UPS" in response
        assert "Current Status: in_transit" in response
        assert "Estimated Delivery:" in response


@pytest.mark.asyncio
async def test_get_order_status_exception_handling():
    """Test get_order_status exception handling."""
    server = EcommerceMCPServer()

    with patch.object(server.ecommerce_strategy, "get_order") as mock_get_order:
        mock_get_order.side_effect = Exception("Database error")

        response = await server.get_order_status("ORD-1001")
        assert "encountered an error" in response


@pytest.mark.asyncio
async def test_cancel_order_already_delivered():
    """Test canceling an already delivered order."""
    server = EcommerceMCPServer()

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
    delivered_order = Order(
        order_id="ORD-DELIVERED",
        customer_id="CUST-100",
        status="delivered",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        entries=[entry],
        total_amount=25.00,
        shipping_address=address,
        billing_address=address,
    )

    with patch.object(server.ecommerce_strategy, "get_order") as mock_get_order:
        mock_get_order.return_value = delivered_order

        response = await server.cancel_order("ORD-DELIVERED")
        assert "cannot be cancelled as it is already delivered" in response


@pytest.mark.asyncio
async def test_cancel_order_already_shipped():
    """Test canceling an already shipped order."""
    server = EcommerceMCPServer()

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
    shipped_order = Order(
        order_id="ORD-SHIPPED",
        customer_id="CUST-100",
        status="shipped",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        entries=[entry],
        total_amount=25.00,
        shipping_address=address,
        billing_address=address,
    )

    with patch.object(server.ecommerce_strategy, "get_order") as mock_get_order:
        mock_get_order.return_value = shipped_order

        response = await server.cancel_order("ORD-SHIPPED")
        assert "has already shipped" in response


@pytest.mark.asyncio
async def test_cancel_order_failure():
    """Test cancel_order when cancellation fails."""
    server = EcommerceMCPServer()

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
    processing_order = Order(
        order_id="ORD-PROCESSING",
        customer_id="CUST-100",
        status="processing",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        entries=[entry],
        total_amount=25.00,
        shipping_address=address,
        billing_address=address,
    )

    with (
        patch.object(server.ecommerce_strategy, "get_order") as mock_get_order,
        patch.object(server.ecommerce_strategy, "cancel_order") as mock_cancel,
    ):

        mock_get_order.return_value = processing_order
        mock_cancel.return_value = False

        response = await server.cancel_order("ORD-PROCESSING")
        assert "Unable to cancel order" in response


@pytest.mark.asyncio
async def test_cancel_order_exception_handling():
    """Test cancel_order exception handling."""
    server = EcommerceMCPServer()

    with patch.object(server.ecommerce_strategy, "get_order") as mock_get_order:
        mock_get_order.side_effect = Exception("Database error")

        response = await server.cancel_order("ORD-1001")
        assert "encountered an error" in response


@pytest.mark.asyncio
async def test_process_return_ineligible_order():
    """Test processing return for order that's not eligible."""
    server = EcommerceMCPServer()

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
    processing_order = Order(
        order_id="ORD-PROCESSING",
        customer_id="CUST-100",
        status="processing",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        entries=[entry],
        total_amount=25.00,
        shipping_address=address,
        billing_address=address,
    )

    with patch.object(server.ecommerce_strategy, "get_order") as mock_get_order:
        mock_get_order.return_value = processing_order

        response = await server.process_return("ORD-PROCESSING")
        assert "cannot be returned yet" in response


@pytest.mark.asyncio
async def test_process_return_failure():
    """Test process_return when return initiation fails."""
    server = EcommerceMCPServer()

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
    delivered_order = Order(
        order_id="ORD-DELIVERED",
        customer_id="CUST-100",
        status="delivered",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        entries=[entry],
        total_amount=25.00,
        shipping_address=address,
        billing_address=address,
    )

    with (
        patch.object(server.ecommerce_strategy, "get_order") as mock_get_order,
        patch.object(server.ecommerce_strategy, "initiate_return") as mock_return,
    ):

        mock_get_order.return_value = delivered_order
        mock_return.return_value = None

        response = await server.process_return("ORD-DELIVERED")
        assert "Unable to process return" in response


@pytest.mark.asyncio
async def test_process_return_exception_handling():
    """Test process_return exception handling."""
    server = EcommerceMCPServer()

    with patch.object(server.ecommerce_strategy, "get_order") as mock_get_order:
        mock_get_order.side_effect = Exception("Database error")

        response = await server.process_return("ORD-1001")
        assert "encountered an error" in response


@pytest.mark.asyncio
async def test_track_package_by_tracking_number():
    """Test tracking by tracking number (not implemented)."""
    server = EcommerceMCPServer()

    response = await server.track_package("TRK123456789", "tracking")
    assert "not yet implemented" in response


@pytest.mark.asyncio
async def test_track_package_exception_handling():
    """Test track_package exception handling."""
    server = EcommerceMCPServer()

    with patch.object(server.ecommerce_strategy, "get_order_tracking") as mock_tracking:
        mock_tracking.side_effect = Exception("Database error")

        response = await server.track_package("ORD-1001")
        assert "encountered an error" in response


@pytest.mark.asyncio
async def test_get_support_info_exception_handling():
    """Test get_support_info exception handling."""
    server = EcommerceMCPServer()

    with patch.object(server.ecommerce_strategy, "get_return_policy") as mock_policy:
        mock_policy.side_effect = Exception("Database error")

        response = await server.get_support_info("returns")
        assert "encountered an error" in response
