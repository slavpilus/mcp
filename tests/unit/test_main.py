"""Test the main FastMCP server module."""

from pathlib import Path
from unittest.mock import Mock, patch

# Import the main module
import main


def test_homepage_success():
    """Test successful homepage loading."""
    # Mock the HTML file content
    mock_html_content = "<h1>Test Homepage</h1>"

    with patch.object(Path, "read_text", return_value=mock_html_content):
        # Mock request object
        mock_request = Mock()

        # Import and test the homepage function
        # Since homepage is async, we need to test it properly
        import asyncio

        from main import homepage

        result = asyncio.run(homepage(mock_request))

        # Check that it returns an HTMLResponse
        assert hasattr(result, "body")
        assert mock_html_content.encode() == result.body


def test_homepage_file_not_found():
    """Test homepage when HTML file is not found."""
    with patch.object(Path, "read_text", side_effect=FileNotFoundError):
        # Mock request object
        mock_request = Mock()

        # Import and test the homepage function
        # Since homepage is async, we need to test it properly
        import asyncio

        from main import homepage

        result = asyncio.run(homepage(mock_request))

        # Check that it returns an HTMLResponse with fallback content
        assert hasattr(result, "body")
        assert result.status_code == 500
        assert b"Enneagora - E-commerce MCP Server" in result.body


def test_get_order_status():
    """Test get_order_status tool function."""
    with patch("main.ecommerce_server") as mock_server:
        mock_server.get_order_status.return_value = "Order ORD-1001 is shipped"

        result = main.get_order_status("ORD-1001", "CUST-100")

        mock_server.get_order_status.assert_called_once_with("ORD-1001", "CUST-100")
        assert result == "Order ORD-1001 is shipped"


def test_cancel_order():
    """Test cancel_order tool function."""
    with patch("main.ecommerce_server") as mock_server:
        mock_server.cancel_order.return_value = "Order ORD-1001 has been cancelled"

        result = main.cancel_order("ORD-1001", "Customer requested", "CUST-100")

        mock_server.cancel_order.assert_called_once_with(
            "ORD-1001", "Customer requested", "CUST-100"
        )
        assert result == "Order ORD-1001 has been cancelled"


def test_process_return():
    """Test process_return tool function."""
    with patch("main.ecommerce_server") as mock_server:
        mock_server.process_return.return_value = "Return initiated with ID RET-001"

        result = main.process_return("ORD-1001", ["ITEM-1"], "Damaged", "CUST-100")

        mock_server.process_return.assert_called_once_with(
            "ORD-1001", ["ITEM-1"], "Damaged", "CUST-100"
        )
        assert result == "Return initiated with ID RET-001"


def test_track_package():
    """Test track_package tool function."""
    with patch("main.ecommerce_server") as mock_server:
        mock_server.track_package.return_value = "Package is in transit"

        result = main.track_package("ORD-1001", "CUST-100")

        mock_server.track_package.assert_called_once_with(
            "ORD-1001", "order", "CUST-100"
        )
        assert result == "Package is in transit"


def test_get_support_info():
    """Test get_support_info tool function."""
    with patch("main.ecommerce_server") as mock_server:
        mock_server.get_support_info.return_value = "General support information"

        result = main.get_support_info("general", "CUST-100")

        mock_server.get_support_info.assert_called_once_with("general", "CUST-100")
        assert result == "General support information"


def test_mcp_server_initialization():
    """Test that the MCP server is properly initialized."""
    # Check that the ecommerce_server is created
    assert main.ecommerce_server is not None

    # Check that the FastMCP instance is created
    assert main.mcp is not None
    assert main.mcp.name == "Enneagora - E-commerce MCP Server"


def test_tool_functions_with_defaults():
    """Test tool functions with default parameters."""
    with patch("main.ecommerce_server") as mock_server:
        mock_server.get_order_status.return_value = "Order status"
        mock_server.cancel_order.return_value = "Order cancelled"
        mock_server.process_return.return_value = "Return processed"
        mock_server.track_package.return_value = "Package tracked"
        mock_server.get_support_info.return_value = "Support info"

        # Test with default parameters
        main.get_order_status("ORD-1001")
        mock_server.get_order_status.assert_called_with("ORD-1001", "default")

        main.cancel_order("ORD-1001")
        mock_server.cancel_order.assert_called_with(
            "ORD-1001", "Customer requested", "default"
        )

        main.process_return("ORD-1001")
        mock_server.process_return.assert_called_with(
            "ORD-1001", None, "Customer return", "default"
        )

        main.track_package("ORD-1001")
        mock_server.track_package.assert_called_with("ORD-1001", "order", "default")

        main.get_support_info()
        mock_server.get_support_info.assert_called_with("general", "default")
