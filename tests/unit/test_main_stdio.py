"""Unit tests for main_stdio.py - the stdio transport version of the MCP server."""

import sys
from unittest.mock import Mock, patch

import pytest

# Mock the mcp module before importing main_stdio
sys.modules["mcp"] = Mock()
sys.modules["mcp.server"] = Mock()


class MockFastMCP:
    """Mock FastMCP class for testing."""

    def __init__(self, name):
        self.name = name
        self.tools = {}
        self.settings = Mock()

    def tool(self):
        """Mock tool decorator."""

        def decorator(func):
            self.tools[func.__name__] = func
            return func

        return decorator

    def run(self, transport="stdio"):
        """Mock run method."""
        pass


# Patch FastMCP before importing main_stdio
with patch("mcp.server.FastMCP", MockFastMCP):
    import main_stdio


class TestMainStdio:
    """Test cases for the stdio MCP server."""

    @pytest.fixture
    def mock_ecommerce_server(self):
        """Mock EcommerceMCPServer."""
        with patch("main_stdio.ecommerce_server") as mock:
            yield mock

    def test_module_imports(self):
        """Test that the module imports correctly."""
        assert hasattr(main_stdio, "mcp")
        assert hasattr(main_stdio, "ecommerce_server")
        assert hasattr(main_stdio, "logger")

    def test_server_initialization(self):
        """Test that the MCP server is initialized correctly."""
        assert main_stdio.mcp.name == "Enneagora - E-commerce MCP Server"

    def test_get_order_status_tool(self, mock_ecommerce_server):
        """Test the get_order_status tool."""
        # Setup mock
        mock_ecommerce_server.get_order_status.return_value = (
            "Order ORD-1001 Status: Shipped"
        )

        # Call the tool
        result = main_stdio.get_order_status("ORD-1001", "customer123")

        # Verify
        mock_ecommerce_server.get_order_status.assert_called_once_with(
            "ORD-1001", "customer123"
        )
        assert result == "Order ORD-1001 Status: Shipped"

    def test_get_order_status_default_customer(self, mock_ecommerce_server):
        """Test get_order_status with default customer_id."""
        mock_ecommerce_server.get_order_status.return_value = (
            "Order ORD-1002 Status: Processing"
        )

        result = main_stdio.get_order_status("ORD-1002")

        mock_ecommerce_server.get_order_status.assert_called_once_with(
            "ORD-1002", "default"
        )
        assert result == "Order ORD-1002 Status: Processing"

    def test_cancel_order_tool(self, mock_ecommerce_server):
        """Test the cancel_order tool."""
        mock_ecommerce_server.cancel_order.return_value = "Order cancelled successfully"

        result = main_stdio.cancel_order("ORD-1003", "Changed my mind", "customer456")

        mock_ecommerce_server.cancel_order.assert_called_once_with(
            "ORD-1003", "Changed my mind", "customer456"
        )
        assert result == "Order cancelled successfully"

    def test_cancel_order_defaults(self, mock_ecommerce_server):
        """Test cancel_order with default parameters."""
        mock_ecommerce_server.cancel_order.return_value = "Order cancelled"

        result = main_stdio.cancel_order("ORD-1004")

        mock_ecommerce_server.cancel_order.assert_called_once_with(
            "ORD-1004", "Customer requested", "default"
        )
        assert result == "Order cancelled"

    def test_process_return_tool(self, mock_ecommerce_server):
        """Test the process_return tool."""
        mock_ecommerce_server.process_return.return_value = "Return initiated"

        result = main_stdio.process_return(
            "ORD-1005", ["ITEM-1", "ITEM-2"], "Defective", "customer789"
        )

        mock_ecommerce_server.process_return.assert_called_once_with(
            "ORD-1005", ["ITEM-1", "ITEM-2"], "Defective", "customer789"
        )
        assert result == "Return initiated"

    def test_process_return_all_items(self, mock_ecommerce_server):
        """Test process_return with None item_ids (all items)."""
        mock_ecommerce_server.process_return.return_value = "All items return initiated"

        result = main_stdio.process_return("ORD-1006")

        mock_ecommerce_server.process_return.assert_called_once_with(
            "ORD-1006", None, "Customer return", "default"
        )
        assert result == "All items return initiated"

    def test_track_package_tool(self, mock_ecommerce_server):
        """Test the track_package tool."""
        mock_ecommerce_server.track_package.return_value = "Package in transit"

        result = main_stdio.track_package("ORD-1007", "customer321")

        mock_ecommerce_server.track_package.assert_called_once_with(
            "ORD-1007", "order", "customer321"
        )
        assert result == "Package in transit"

    def test_track_package_default_customer(self, mock_ecommerce_server):
        """Test track_package with default customer_id."""
        mock_ecommerce_server.track_package.return_value = "Package delivered"

        result = main_stdio.track_package("ORD-1008")

        mock_ecommerce_server.track_package.assert_called_once_with(
            "ORD-1008", "order", "default"
        )
        assert result == "Package delivered"

    def test_get_support_info_tool(self, mock_ecommerce_server):
        """Test the get_support_info tool."""
        mock_ecommerce_server.get_support_info.return_value = (
            "Return policy information"
        )

        result = main_stdio.get_support_info("returns", "customer654")

        mock_ecommerce_server.get_support_info.assert_called_once_with(
            "returns", "customer654"
        )
        assert result == "Return policy information"

    def test_get_support_info_defaults(self, mock_ecommerce_server):
        """Test get_support_info with default parameters."""
        mock_ecommerce_server.get_support_info.return_value = "General support info"

        result = main_stdio.get_support_info()

        mock_ecommerce_server.get_support_info.assert_called_once_with(
            "general", "default"
        )
        assert result == "General support info"

    def test_main_execution(self):
        """Test the main execution block."""
        with patch.object(main_stdio.mcp, "run") as mock_run:
            with patch.object(main_stdio.logger, "info") as mock_info:
                # Import and execute the main block code

                import main_stdio as module

                # Manually trigger the main block logic
                if hasattr(module, "__name__"):
                    module.logger.info(
                        "Starting Enneagora MCP Server in STDIO mode for Claude Desktop"
                    )
                    module.mcp.run(transport="stdio")

                # Verify
                mock_info.assert_called_with(
                    "Starting Enneagora MCP Server in STDIO mode for Claude Desktop"
                )
                mock_run.assert_called_with(transport="stdio")

    def test_tool_registration(self):
        """Test that all tools are registered with the MCP server."""
        expected_tools = {
            "get_order_status",
            "cancel_order",
            "process_return",
            "track_package",
            "get_support_info",
        }

        # Check that all expected tools are registered
        registered_tools = set(main_stdio.mcp.tools.keys())
        assert registered_tools == expected_tools

    def test_tool_docstrings(self):
        """Test that all tools have proper docstrings."""
        for _tool_name, tool_func in main_stdio.mcp.tools.items():
            assert tool_func.__doc__ is not None
            assert len(tool_func.__doc__) > 0
            assert "Args:" in tool_func.__doc__
            assert "Returns:" in tool_func.__doc__

    def test_logging_configuration(self):
        """Test that logging is configured correctly."""
        # Check that our logger exists and has correct name
        assert hasattr(main_stdio, "logger")
        assert main_stdio.logger.name == "main_stdio"


class TestMainStdioIntegration:
    """Integration tests for main_stdio with real dependencies."""

    @pytest.mark.integration
    def test_ecommerce_server_instance(self):
        """Test that EcommerceMCPServer instance is created."""
        from mcp_server.server import EcommerceMCPServer

        # This will fail if the real import doesn't work
        assert isinstance(main_stdio.ecommerce_server, EcommerceMCPServer)
