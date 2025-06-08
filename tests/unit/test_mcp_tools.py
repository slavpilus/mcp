"""Test the MCP tools registration module."""

from unittest.mock import AsyncMock, Mock, patch

import pytest

from mcp_server.mcp_tools import register_tools


@pytest.fixture
def mock_mcp_instance():
    """Create a mock FastMCP instance."""
    mock_mcp = Mock()
    # Mock the tool decorator to return the function unchanged
    mock_mcp.tool = Mock(side_effect=lambda: lambda func: func)
    return mock_mcp


@pytest.fixture
def mock_ecommerce_server():
    """Create a mock EcommerceMCPServer."""
    with patch("mcp_server.mcp_tools.ecommerce_server") as mock_server:
        mock_server.get_order_status = AsyncMock(return_value="Order status response")
        mock_server.cancel_order = AsyncMock(return_value="Order cancelled")
        mock_server.process_return = AsyncMock(return_value="Return processed")
        mock_server.track_package = AsyncMock(return_value="Package tracked")
        mock_server.get_support_info = AsyncMock(return_value="Support info")
        yield mock_server


@pytest.mark.asyncio
async def test_register_tools_returns_tool_dict(mock_mcp_instance):
    """Test that register_tools returns a dictionary of tool functions."""
    tools = register_tools(mock_mcp_instance)

    # Check that all expected tools are returned
    expected_tools = {
        "get_order_status",
        "cancel_order",
        "process_return",
        "track_package",
        "get_support_info",
    }

    assert isinstance(tools, dict)
    assert set(tools.keys()) == expected_tools

    # Check that all tools are callable
    for tool_name, tool_func in tools.items():
        assert callable(tool_func), f"{tool_name} should be callable"


@pytest.mark.asyncio
async def test_register_tools_calls_mcp_tool_decorator(mock_mcp_instance):
    """Test that register_tools calls mcp.tool() for each tool."""
    register_tools(mock_mcp_instance)

    # Verify that mcp.tool() was called 5 times (once for each tool)
    assert mock_mcp_instance.tool.call_count == 5


@pytest.mark.asyncio
async def test_get_order_status_tool(mock_mcp_instance, mock_ecommerce_server):
    """Test the get_order_status tool function."""
    tools = register_tools(mock_mcp_instance)

    result = await tools["get_order_status"]("ORD-1001", "CUST-100")

    mock_ecommerce_server.get_order_status.assert_called_once_with(
        "ORD-1001", "CUST-100"
    )
    assert result == "Order status response"


@pytest.mark.asyncio
async def test_get_order_status_with_defaults(mock_mcp_instance, mock_ecommerce_server):
    """Test get_order_status with default customer_id."""
    tools = register_tools(mock_mcp_instance)

    result = await tools["get_order_status"]("ORD-1001")

    mock_ecommerce_server.get_order_status.assert_called_once_with(
        "ORD-1001", "default"
    )
    assert result == "Order status response"


@pytest.mark.asyncio
async def test_cancel_order_tool(mock_mcp_instance, mock_ecommerce_server):
    """Test the cancel_order tool function."""
    tools = register_tools(mock_mcp_instance)

    result = await tools["cancel_order"]("ORD-1001", "Customer requested", "CUST-100")

    mock_ecommerce_server.cancel_order.assert_called_once_with(
        "ORD-1001", "Customer requested", "CUST-100"
    )
    assert result == "Order cancelled"


@pytest.mark.asyncio
async def test_cancel_order_with_defaults(mock_mcp_instance, mock_ecommerce_server):
    """Test cancel_order with default parameters."""
    tools = register_tools(mock_mcp_instance)

    result = await tools["cancel_order"]("ORD-1001")

    mock_ecommerce_server.cancel_order.assert_called_once_with(
        "ORD-1001", "Customer requested", "default"
    )
    assert result == "Order cancelled"


@pytest.mark.asyncio
async def test_process_return_tool(mock_mcp_instance, mock_ecommerce_server):
    """Test the process_return tool function."""
    tools = register_tools(mock_mcp_instance)

    result = await tools["process_return"](
        "ORD-1001", ["ITEM-1"], "Damaged", "CUST-100"
    )

    mock_ecommerce_server.process_return.assert_called_once_with(
        "ORD-1001", ["ITEM-1"], "Damaged", "CUST-100"
    )
    assert result == "Return processed"


@pytest.mark.asyncio
async def test_process_return_with_defaults(mock_mcp_instance, mock_ecommerce_server):
    """Test process_return with default parameters."""
    tools = register_tools(mock_mcp_instance)

    result = await tools["process_return"]("ORD-1001")

    mock_ecommerce_server.process_return.assert_called_once_with(
        "ORD-1001", None, "Customer return", "default"
    )
    assert result == "Return processed"


@pytest.mark.asyncio
async def test_track_package_tool(mock_mcp_instance, mock_ecommerce_server):
    """Test the track_package tool function."""
    tools = register_tools(mock_mcp_instance)

    result = await tools["track_package"]("ORD-1001", "CUST-100")

    mock_ecommerce_server.track_package.assert_called_once_with(
        "ORD-1001", "order", "CUST-100"
    )
    assert result == "Package tracked"


@pytest.mark.asyncio
async def test_track_package_with_defaults(mock_mcp_instance, mock_ecommerce_server):
    """Test track_package with default customer_id."""
    tools = register_tools(mock_mcp_instance)

    result = await tools["track_package"]("ORD-1001")

    mock_ecommerce_server.track_package.assert_called_once_with(
        "ORD-1001", "order", "default"
    )
    assert result == "Package tracked"


@pytest.mark.asyncio
async def test_get_support_info_tool(mock_mcp_instance, mock_ecommerce_server):
    """Test the get_support_info tool function."""
    tools = register_tools(mock_mcp_instance)

    result = await tools["get_support_info"]("returns", "CUST-100")

    mock_ecommerce_server.get_support_info.assert_called_once_with(
        "returns", "CUST-100"
    )
    assert result == "Support info"


@pytest.mark.asyncio
async def test_get_support_info_with_defaults(mock_mcp_instance, mock_ecommerce_server):
    """Test get_support_info with default parameters."""
    tools = register_tools(mock_mcp_instance)

    result = await tools["get_support_info"]()

    mock_ecommerce_server.get_support_info.assert_called_once_with("general", "default")
    assert result == "Support info"


@pytest.mark.asyncio
async def test_tool_function_signatures(mock_mcp_instance):
    """Test that tool functions have correct signatures and docstrings."""
    tools = register_tools(mock_mcp_instance)

    # Test get_order_status signature
    get_order_status = tools["get_order_status"]
    assert get_order_status.__name__ == "get_order_status"
    assert "Get status for a specific order" in get_order_status.__doc__
    assert "order_id" in get_order_status.__doc__
    assert "customer_id" in get_order_status.__doc__

    # Test cancel_order signature
    cancel_order = tools["cancel_order"]
    assert cancel_order.__name__ == "cancel_order"
    assert "Cancel an order" in cancel_order.__doc__
    assert "reason" in cancel_order.__doc__

    # Test process_return signature
    process_return = tools["process_return"]
    assert process_return.__name__ == "process_return"
    assert "Process a return request" in process_return.__doc__
    assert "item_ids" in process_return.__doc__

    # Test track_package signature
    track_package = tools["track_package"]
    assert track_package.__name__ == "track_package"
    assert "Track package delivery status" in track_package.__doc__

    # Test get_support_info signature
    get_support_info = tools["get_support_info"]
    assert get_support_info.__name__ == "get_support_info"
    assert "Get customer support information" in get_support_info.__doc__
    assert "topic" in get_support_info.__doc__


@pytest.mark.asyncio
async def test_ecommerce_server_initialization():
    """Test that the ecommerce_server is properly initialized."""
    from mcp_server.mcp_tools import ecommerce_server

    assert ecommerce_server is not None
    # The server should have the expected strategy
    assert hasattr(ecommerce_server, "ecommerce_strategy")
    assert ecommerce_server.ecommerce_strategy is not None


@pytest.mark.asyncio
async def test_tool_execution_paths(mock_mcp_instance, mock_ecommerce_server):
    """Test that the tool functions actually execute their implementation paths."""
    tools = register_tools(mock_mcp_instance)

    # Test all tool execution paths
    await tools["get_order_status"]("ORD-1001", "CUST-100")
    await tools["cancel_order"]("ORD-1001", "reason", "CUST-100")
    await tools["process_return"]("ORD-1001", ["item1"], "reason", "CUST-100")
    await tools["track_package"]("ORD-1001", "CUST-100")
    await tools["get_support_info"]("topic", "CUST-100")

    # Verify all calls were made
    mock_ecommerce_server.get_order_status.assert_called()
    mock_ecommerce_server.cancel_order.assert_called()
    mock_ecommerce_server.process_return.assert_called()
    mock_ecommerce_server.track_package.assert_called()
    mock_ecommerce_server.get_support_info.assert_called()
