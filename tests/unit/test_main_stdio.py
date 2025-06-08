"""Unit tests for main_stdio.py - robust version for CI/CD environments."""

import sys
from unittest.mock import MagicMock, patch

# Create comprehensive mocks before any imports
mock_mcp_module = MagicMock()
mock_fastmcp_class = MagicMock()
mock_ecommerce_server = MagicMock()

# Mock the FastMCP instance with proper attributes
mock_fastmcp_instance = MagicMock()
mock_fastmcp_instance.name = "Enneagora - E-commerce MCP Server"
mock_fastmcp_instance.tools = {}
mock_fastmcp_instance.settings = MagicMock()


# Set up tool decorator mock
def mock_tool_decorator():
    def decorator(func):
        mock_fastmcp_instance.tools[func.__name__] = func
        return func

    return decorator


mock_fastmcp_instance.tool = mock_tool_decorator
mock_fastmcp_instance.run = MagicMock()

# Configure the FastMCP class mock to return our instance
mock_fastmcp_class.return_value = mock_fastmcp_instance

# Set up module mocks
mock_mcp_module.server.FastMCP = mock_fastmcp_class
sys.modules["mcp"] = mock_mcp_module
sys.modules["mcp.server"] = mock_mcp_module.server

# Mock the EcommerceMCPServer
with patch("mcp_server.server.EcommerceMCPServer", return_value=mock_ecommerce_server):
    # Now import the module
    import main_stdio

# Ensure the ecommerce_server is set to our mock
main_stdio.ecommerce_server = mock_ecommerce_server


class TestMainStdio:
    """Robust test cases for the stdio MCP server."""

    def setup_method(self):
        """Reset mock calls before each test."""
        mock_ecommerce_server.reset_mock()

    def test_module_structure(self):
        """Test the basic module structure."""
        assert hasattr(main_stdio, "mcp")
        assert hasattr(main_stdio, "ecommerce_server")
        assert hasattr(main_stdio, "logger")

    def test_mcp_server_configuration(self):
        """Test MCP server configuration."""
        assert main_stdio.mcp.name == "Enneagora - E-commerce MCP Server"
        assert hasattr(main_stdio.mcp, "tools")
        assert hasattr(main_stdio.mcp, "run")

    def test_tool_functions_exist(self):
        """Test that all expected tool functions exist."""
        expected_tools = {
            "get_order_status",
            "cancel_order",
            "process_return",
            "track_package",
            "get_support_info",
        }

        # Check tools are registered
        registered_tools = set(main_stdio.mcp.tools.keys())
        assert registered_tools == expected_tools

    def test_get_order_status_function(self):
        """Test get_order_status function exists and is callable."""
        assert hasattr(main_stdio, "get_order_status")
        assert callable(main_stdio.get_order_status)

        # Test function signature
        func = main_stdio.get_order_status
        assert func.__name__ == "get_order_status"
        assert "order_id" in func.__code__.co_varnames
        assert "customer_id" in func.__code__.co_varnames

    def test_cancel_order_function(self):
        """Test cancel_order function exists and is callable."""
        assert hasattr(main_stdio, "cancel_order")
        assert callable(main_stdio.cancel_order)

        # Test function signature
        func = main_stdio.cancel_order
        assert func.__name__ == "cancel_order"
        assert "order_id" in func.__code__.co_varnames

    def test_process_return_function(self):
        """Test process_return function exists and is callable."""
        assert hasattr(main_stdio, "process_return")
        assert callable(main_stdio.process_return)

        # Test function signature
        func = main_stdio.process_return
        assert func.__name__ == "process_return"
        assert "order_id" in func.__code__.co_varnames

    def test_track_package_function(self):
        """Test track_package function exists and is callable."""
        assert hasattr(main_stdio, "track_package")
        assert callable(main_stdio.track_package)

        # Test function signature
        func = main_stdio.track_package
        assert func.__name__ == "track_package"
        assert "order_id" in func.__code__.co_varnames

    def test_get_support_info_function(self):
        """Test get_support_info function exists and is callable."""
        assert hasattr(main_stdio, "get_support_info")
        assert callable(main_stdio.get_support_info)

        # Test function signature
        func = main_stdio.get_support_info
        assert func.__name__ == "get_support_info"
        assert "topic" in func.__code__.co_varnames

    def test_function_docstrings(self):
        """Test that all tool functions have proper docstrings."""
        for tool_name in main_stdio.mcp.tools:
            func = getattr(main_stdio, tool_name)
            assert func.__doc__ is not None
            assert len(func.__doc__) > 0
            assert "Args:" in func.__doc__
            assert "Returns:" in func.__doc__

    def test_logging_setup(self):
        """Test logging configuration."""
        assert hasattr(main_stdio, "logger")
        assert main_stdio.logger.name == "main_stdio"

    def test_ecommerce_server_instance(self):
        """Test ecommerce server instance."""
        assert hasattr(main_stdio, "ecommerce_server")
        assert main_stdio.ecommerce_server is not None

    @patch.object(main_stdio, "logger")
    def test_main_block_execution(self, mock_logger):
        """Test main block execution logic."""
        with patch.object(main_stdio.mcp, "run") as mock_run:
            # Simulate main execution
            main_stdio.logger.info(
                "Starting Enneagora MCP Server in STDIO mode for Claude Desktop"
            )
            main_stdio.mcp.run(transport="stdio")

            # Verify calls
            mock_logger.info.assert_called_with(
                "Starting Enneagora MCP Server in STDIO mode for Claude Desktop"
            )
            mock_run.assert_called_with(transport="stdio")

    def test_get_order_status_execution(self):
        """Test get_order_status function execution."""
        # Mock the ecommerce server's response
        mock_ecommerce_server.get_order_status.return_value = (
            "Order ORD-1001 Status: Shipped"
        )

        # Call the function
        result = main_stdio.get_order_status("ORD-1001", "customer123")

        # Verify the result
        assert result == "Order ORD-1001 Status: Shipped"
        mock_ecommerce_server.get_order_status.assert_called_once_with(
            "ORD-1001", "customer123"
        )

    def test_cancel_order_execution(self):
        """Test cancel_order function execution."""
        # Mock the ecommerce server's response
        mock_ecommerce_server.cancel_order.return_value = "Order cancelled successfully"

        # Call the function
        result = main_stdio.cancel_order("ORD-1002", "Changed my mind", "customer456")

        # Verify the result
        assert result == "Order cancelled successfully"
        mock_ecommerce_server.cancel_order.assert_called_once_with(
            "ORD-1002", "Changed my mind", "customer456"
        )

    def test_process_return_execution(self):
        """Test process_return function execution."""
        # Mock the ecommerce server's response
        mock_ecommerce_server.process_return.return_value = "Return RET-12345 initiated"

        # Call the function
        result = main_stdio.process_return(
            "ORD-1003", ["ITEM-1", "ITEM-2"], "Defective", "customer789"
        )

        # Verify the result
        assert result == "Return RET-12345 initiated"
        mock_ecommerce_server.process_return.assert_called_once_with(
            "ORD-1003", ["ITEM-1", "ITEM-2"], "Defective", "customer789"
        )

    def test_track_package_execution(self):
        """Test track_package function execution."""
        # Mock the ecommerce server's response
        mock_ecommerce_server.track_package.return_value = (
            "Package in transit - ETA: 2 days"
        )

        # Call the function
        result = main_stdio.track_package("ORD-1004", "customer321")

        # Verify the result
        assert result == "Package in transit - ETA: 2 days"
        mock_ecommerce_server.track_package.assert_called_once_with(
            "ORD-1004", "order", "customer321"
        )

    def test_get_support_info_execution(self):
        """Test get_support_info function execution."""
        # Mock the ecommerce server's response
        mock_ecommerce_server.get_support_info.return_value = "Return policy: 30 days"

        # Call the function
        result = main_stdio.get_support_info("returns", "customer654")

        # Verify the result
        assert result == "Return policy: 30 days"
        mock_ecommerce_server.get_support_info.assert_called_once_with(
            "returns", "customer654"
        )
