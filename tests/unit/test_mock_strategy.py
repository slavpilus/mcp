import pytest

from mcp_server.strategies.mock_strategy import MockDataStrategy


@pytest.mark.asyncio
async def test_mock_strategy_initialization():
    """Test MockDataStrategy initialization."""
    strategy = MockDataStrategy()
    assert len(strategy.orders) == 20  # Should create 20 sample orders
    assert len(strategy.returns) == 0  # No returns initially


@pytest.mark.asyncio
async def test_get_order():
    """Test getting an order by ID."""
    strategy = MockDataStrategy()

    # Get first order ID
    order_id = list(strategy.orders.keys())[0]
    order = await strategy.get_order(order_id)

    assert order is not None
    assert order.order_id == order_id
    assert len(order.entries) > 0
    assert order.shipping_address is not None
    assert order.billing_address is not None

    # Test error pattern order (should return None)
    order = await strategy.get_order("ORD-1234-E")
    assert order is None

    # Test dynamic order creation (should create pending order)
    order = await strategy.get_order("ORD-9999")
    assert order is not None
    assert order.order_id == "ORD-9999"
    assert order.status == "pending"


@pytest.mark.asyncio
async def test_get_customer_orders():
    """Test getting orders for a customer."""
    strategy = MockDataStrategy()

    # Get a customer ID from existing orders
    customer_id = list(strategy.orders.values())[0].customer_id
    orders = await strategy.get_customer_orders(customer_id)

    assert isinstance(orders, list)
    assert all(order.customer_id == customer_id for order in orders)

    # Test with filters
    if orders:
        status = orders[0].status
        filtered_orders = await strategy.get_customer_orders(
            customer_id, {"status": status}
        )
        assert all(order.status == status for order in filtered_orders)


@pytest.mark.asyncio
async def test_update_order_status():
    """Test updating order status."""
    strategy = MockDataStrategy()
    order_id = list(strategy.orders.keys())[0]

    success = await strategy.update_order_status(order_id, "shipped")
    assert success is True

    order = await strategy.get_order(order_id)
    assert order.status == "shipped"

    # Test error pattern order (should fail)
    success = await strategy.update_order_status("ORD-ERROR", "shipped")
    assert success is False


@pytest.mark.asyncio
async def test_cancel_order():
    """Test cancelling an order."""
    strategy = MockDataStrategy()

    # Find a pending or processing order
    cancellable_order = None
    for order in strategy.orders.values():
        if order.status in ["pending", "processing"]:
            cancellable_order = order
            break

    if cancellable_order:
        success = await strategy.cancel_order(
            cancellable_order.order_id, "Changed mind"
        )
        assert success is True

        order = await strategy.get_order(cancellable_order.order_id)
        assert order.status == "cancelled"

    # Test cancelling shipped order (should fail)
    shipped_order = None
    for order in strategy.orders.values():
        if order.status == "shipped":
            shipped_order = order
            break

    if shipped_order:
        success = await strategy.cancel_order(shipped_order.order_id, "Too late")
        assert success is False


@pytest.mark.asyncio
async def test_initiate_return():
    """Test initiating a return."""
    strategy = MockDataStrategy()
    order_id = list(strategy.orders.keys())[0]

    return_obj = await strategy.initiate_return(order_id, ["ENTRY-001"], "Damaged item")

    assert return_obj is not None
    assert return_obj.order_id == order_id
    assert return_obj.status == "initiated"
    assert return_obj.reason == "Damaged item"
    assert len(return_obj.items) == 1


@pytest.mark.asyncio
async def test_get_order_tracking():
    """Test getting order tracking."""
    strategy = MockDataStrategy()

    # Find an order with tracking
    tracked_order = None
    for order in strategy.orders.values():
        if order.tracking_number:
            tracked_order = order
            break

    if tracked_order:
        tracking = await strategy.get_order_tracking(tracked_order.order_id)
        assert tracking is not None
        assert tracking.tracking_number == tracked_order.tracking_number
        assert tracking.carrier in ["UPS", "FedEx", "USPS", "DHL"]
        assert len(tracking.history) > 0

    # Test order without tracking
    untracked_order = None
    for order in strategy.orders.values():
        if not order.tracking_number:
            untracked_order = order
            break

    if untracked_order:
        tracking = await strategy.get_order_tracking(untracked_order.order_id)
        assert tracking is None


@pytest.mark.asyncio
async def test_search_orders():
    """Test searching orders."""
    strategy = MockDataStrategy()

    # Search by order ID
    order_id = list(strategy.orders.keys())[0]
    results = await strategy.search_orders({"order_id": order_id[:5]})  # Partial match
    assert len(results) > 0

    # Search by customer ID
    customer_id = list(strategy.orders.values())[0].customer_id
    results = await strategy.search_orders({"customer_id": customer_id})
    assert all(order.customer_id == customer_id for order in results)

    # Search by status
    results = await strategy.search_orders({"status": "pending"})
    assert all(order.status == "pending" for order in results)


@pytest.mark.asyncio
async def test_get_return_policy():
    """Test getting return policy."""
    strategy = MockDataStrategy()
    policy = await strategy.get_return_policy()

    assert isinstance(policy, str)
    assert "30-day return policy" in policy
    assert "Return Policy" in policy


@pytest.mark.asyncio
async def test_get_shipping_options():
    """Test getting shipping options."""
    strategy = MockDataStrategy()
    order_id = list(strategy.orders.keys())[0]

    options = await strategy.get_shipping_options(order_id)
    assert len(options) == 3
    assert any(opt.option_id == "standard" for opt in options)
    assert any(opt.option_id == "express" for opt in options)
    assert any(opt.option_id == "overnight" for opt in options)


@pytest.mark.asyncio
async def test_dynamic_order_patterns():
    """Test dynamic order ID patterns."""
    strategy = MockDataStrategy()

    # Test delivered order pattern
    order = await strategy.get_order("ORD-2001-D")
    assert order is not None
    assert order.status == "delivered"
    assert order.tracking_number is not None

    # Test cancelled order pattern
    order = await strategy.get_order("ORD-2002-C")
    assert order is not None
    assert order.status == "cancelled"

    # Test shipped order pattern
    order = await strategy.get_order("ORD-2003-S")
    assert order is not None
    assert order.status == "shipped"
    assert order.tracking_number is not None

    # Test processing order pattern
    order = await strategy.get_order("ORD-2004-P")
    assert order is not None
    assert order.status == "processing"

    # Test failed order pattern
    order = await strategy.get_order("ORD-2005-F")
    assert order is not None
    assert order.status == "failed"

    # Test ready for pickup pattern
    order = await strategy.get_order("ORD-2006-R")
    assert order is not None
    assert order.status == "ready_for_pickup"

    # Test in transit pattern
    order = await strategy.get_order("ORD-2007-T")
    assert order is not None
    assert order.status == "in_transit"
    assert order.tracking_number is not None


@pytest.mark.asyncio
async def test_dynamic_cancel_order_behaviors():
    """Test dynamic cancellation behaviors."""
    strategy = MockDataStrategy()

    # Test cancelling a processing order (should succeed)
    success = await strategy.cancel_order("ORD-3001-P", "Customer requested")
    assert success is True

    # Test cancelling a failed order (should fail)
    success = await strategy.cancel_order("ORD-3002-F", "Customer requested")
    assert success is False

    # Test cancelling a delivered order (should fail)
    success = await strategy.cancel_order("ORD-3003-D", "Customer requested")
    assert success is False

    # Test cancelling a shipped order (should fail)
    success = await strategy.cancel_order("ORD-3004-S", "Customer requested")
    assert success is False


@pytest.mark.asyncio
async def test_dynamic_tracking_behaviors():
    """Test dynamic tracking behaviors."""
    strategy = MockDataStrategy()

    # Test tracking for error order (should return None)
    tracking = await strategy.get_order_tracking("ORD-4001-E")
    assert tracking is None

    # Test tracking for failed order (should return "lost" status)
    tracking = await strategy.get_order_tracking("ORD-4002-F")
    assert tracking is not None
    assert tracking.status == "lost"

    # Test tracking for delivered order
    tracking = await strategy.get_order_tracking("ORD-4003-D")
    assert tracking is not None
    assert tracking.status == "delivered"

    # Test tracking for in transit order
    tracking = await strategy.get_order_tracking("ORD-4004-T")
    assert tracking is not None
    assert tracking.status == "in_transit"
