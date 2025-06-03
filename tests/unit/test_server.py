import pytest

from mcp_server.server import MCPServer
from mcp_server.strategies.mock_strategy import MockDataStrategy


@pytest.mark.asyncio
async def test_mcp_server_initialization():
    """Test MCPServer initialization."""
    # With default strategy
    server = MCPServer()
    assert isinstance(server.strategy, MockDataStrategy)
    assert server._context == {}

    # With custom strategy
    custom_strategy = MockDataStrategy()
    server = MCPServer(strategy=custom_strategy)
    assert server.strategy is custom_strategy


@pytest.mark.asyncio
async def test_process_request_get_order():
    """Test processing get_order request."""
    server = MCPServer()

    # Get a valid order ID from the mock strategy
    order_id = list(server.strategy.orders.keys())[0]

    # Test successful get_order request
    request = {"intent": "get_order", "order_id": order_id}
    response = await server.process_request(request)

    assert response["success"] is True
    assert response["order"] is not None
    assert response["order"]["order_id"] == order_id

    # Test get_order with invalid ID
    request = {"intent": "get_order", "order_id": "INVALID-ID"}
    response = await server.process_request(request)

    assert response["success"] is True
    assert response["order"] is None

    # Test get_order without order_id
    request = {"intent": "get_order"}
    response = await server.process_request(request)

    assert response["success"] is False
    assert "error" in response


@pytest.mark.asyncio
async def test_process_request_unknown_intent():
    """Test processing request with unknown intent."""
    server = MCPServer()

    request = {"intent": "unknown_intent"}
    response = await server.process_request(request)

    assert response["success"] is False
    assert response["error"] == "Unknown intent"

    # Test without intent
    request = {}
    response = await server.process_request(request)

    assert response["success"] is False
    assert response["error"] == "Unknown intent"


def test_context_management():
    """Test context update and retrieval."""
    server = MCPServer()

    # Test initial empty context
    assert server.get_context() == {}

    # Test updating context
    context_data = {"user_id": "123", "session": "abc"}
    server.update_context(context_data)

    retrieved_context = server.get_context()
    assert retrieved_context == context_data

    # Test that get_context returns a copy
    retrieved_context["modified"] = True
    assert "modified" not in server._context

    # Test updating with additional data
    server.update_context({"extra": "data"})
    final_context = server.get_context()
    assert final_context == {"user_id": "123", "session": "abc", "extra": "data"}
