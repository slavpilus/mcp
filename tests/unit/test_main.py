"""Test the main Gradio MCP server module."""

from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

# Import the main module
import main


def test_gradio_interface_creation():
    """Test that the Gradio interface can be created successfully."""
    # Test that create_gradio_interface returns a Gradio Blocks object
    demo = main.create_gradio_interface()

    # Check that it returns a Gradio Blocks instance
    import gradio as gr

    assert isinstance(demo, gr.Blocks)


def test_html_content_loading():
    """Test that HTML content loads successfully from static file."""
    # Mock the HTML file content
    mock_html_content = "<html><body><h1>Test Homepage</h1></body></html>"

    with patch.object(Path, "read_text", return_value=mock_html_content):
        demo = main.create_gradio_interface()
        assert demo is not None


def test_html_content_with_body_extraction():
    """Test HTML content extraction between body tags."""
    mock_html_content = "<html><head><title>Test</title></head><body class='test'><h1>Test Content</h1><p>Some content</p></body></html>"

    with patch.object(Path, "read_text", return_value=mock_html_content):
        demo = main.create_gradio_interface()
        assert demo is not None


def test_html_content_no_body_tag():
    """Test HTML content fallback when no body tag is found."""
    mock_html_content = (
        "<html><head><title>Test</title></head><div>No body tag here</div></html>"
    )

    with patch.object(Path, "read_text", return_value=mock_html_content):
        demo = main.create_gradio_interface()
        assert demo is not None


def test_html_content_file_not_found():
    """Test fallback HTML content when static file is not found."""
    with patch.object(
        Path, "read_text", side_effect=FileNotFoundError("File not found")
    ):
        demo = main.create_gradio_interface()
        assert demo is not None


def test_tools_availability():
    """Test that all MCP tools are available as standalone functions."""
    # Check that TOOLS list was created
    assert main.TOOLS is not None
    assert isinstance(main.TOOLS, list)

    # Check that all expected tools are available
    expected_tools = [
        "get_order_status",
        "cancel_order",
        "process_return",
        "track_package",
        "get_support_info",
        "get_return_policy",
        "get_shipping_info",
        "get_contact_information",
        "get_size_guide",
        "get_warranty_information",
        "get_payment_information",
        "get_account_help",
        "get_loyalty_program_info",
        "get_product_care_info",
    ]

    # Check each tool exists as a function in main module
    for tool_name in expected_tools:
        assert hasattr(main, tool_name), f"{tool_name} should exist in main module"
        tool_func = getattr(main, tool_name)
        assert callable(tool_func), f"{tool_name} should be callable"

    # Check that TOOLS list has the right number of tools
    assert len(main.TOOLS) == 14


def test_ecommerce_server_initialization():
    """Test that the e-commerce server is properly initialized."""
    # Check that the EcommerceMCPServer instance is created
    assert main.ecommerce_server is not None

    # Check it has the expected type
    from mcp_server.server import EcommerceMCPServer

    assert isinstance(main.ecommerce_server, EcommerceMCPServer)


# Test async MCP tool wrapper functions
@patch("main.ecommerce_server")
@pytest.mark.asyncio
async def test_get_order_status(mock_server):
    """Test get_order_status wrapper function."""
    mock_server.get_order_status = AsyncMock(return_value="Order status: Shipped")

    result = await main.get_order_status("12345", "customer123")

    mock_server.get_order_status.assert_called_once_with("12345", "customer123")
    assert result == "Order status: Shipped"


@patch("main.ecommerce_server")
@pytest.mark.asyncio
async def test_get_order_status_default_customer(mock_server):
    """Test get_order_status with default customer."""
    mock_server.get_order_status = AsyncMock(return_value="Order status: Processing")

    result = await main.get_order_status("12345")

    mock_server.get_order_status.assert_called_once_with("12345", "default")
    assert result == "Order status: Processing"


@patch("main.ecommerce_server")
@pytest.mark.asyncio
async def test_cancel_order(mock_server):
    """Test cancel_order wrapper function."""
    mock_server.cancel_order = AsyncMock(return_value="Order cancelled successfully")

    result = await main.cancel_order("12345", "Changed mind", "customer123")

    mock_server.cancel_order.assert_called_once_with(
        "12345", "Changed mind", "customer123"
    )
    assert result == "Order cancelled successfully"


@patch("main.ecommerce_server")
@pytest.mark.asyncio
async def test_cancel_order_defaults(mock_server):
    """Test cancel_order with default parameters."""
    mock_server.cancel_order = AsyncMock(return_value="Order cancelled")

    result = await main.cancel_order("12345")

    mock_server.cancel_order.assert_called_once_with(
        "12345", "Customer requested", "default"
    )
    assert result == "Order cancelled"


@patch("main.ecommerce_server")
@pytest.mark.asyncio
async def test_process_return(mock_server):
    """Test process_return wrapper function."""
    mock_server.process_return = AsyncMock(return_value="Return processed")

    result = await main.process_return(
        "12345", "item1,item2", "Defective", "customer123"
    )

    mock_server.process_return.assert_called_once_with(
        "12345", ["item1", "item2"], "Defective", "customer123"
    )
    assert result == "Return processed"


@patch("main.ecommerce_server")
@pytest.mark.asyncio
async def test_process_return_empty_items(mock_server):
    """Test process_return with empty item list."""
    mock_server.process_return = AsyncMock(return_value="Return processed")

    result = await main.process_return("12345", "", "Defective", "customer123")

    mock_server.process_return.assert_called_once_with(
        "12345", None, "Defective", "customer123"
    )
    assert result == "Return processed"


@patch("main.ecommerce_server")
@pytest.mark.asyncio
async def test_process_return_defaults(mock_server):
    """Test process_return with default parameters."""
    mock_server.process_return = AsyncMock(return_value="Return processed")

    result = await main.process_return("12345")

    mock_server.process_return.assert_called_once_with(
        "12345", None, "Customer return", "default"
    )
    assert result == "Return processed"


@patch("main.ecommerce_server")
@pytest.mark.asyncio
async def test_track_package(mock_server):
    """Test track_package wrapper function."""
    mock_server.track_package = AsyncMock(return_value="Package tracking info")

    result = await main.track_package("12345", "customer123")

    mock_server.track_package.assert_called_once_with("12345", "order", "customer123")
    assert result == "Package tracking info"


@patch("main.ecommerce_server")
@pytest.mark.asyncio
async def test_track_package_default_customer(mock_server):
    """Test track_package with default customer."""
    mock_server.track_package = AsyncMock(return_value="Package status")

    result = await main.track_package("12345")

    mock_server.track_package.assert_called_once_with("12345", "order", "default")
    assert result == "Package status"


@patch("main.ecommerce_server")
@pytest.mark.asyncio
async def test_get_support_info(mock_server):
    """Test get_support_info wrapper function."""
    mock_server.get_support_info = AsyncMock(return_value="Support information")

    result = await main.get_support_info("billing", "customer123")

    mock_server.get_support_info.assert_called_once_with("billing", "customer123")
    assert result == "Support information"


@patch("main.ecommerce_server")
@pytest.mark.asyncio
async def test_get_support_info_defaults(mock_server):
    """Test get_support_info with default parameters."""
    mock_server.get_support_info = AsyncMock(return_value="General support")

    result = await main.get_support_info()

    mock_server.get_support_info.assert_called_once_with("general", "default")
    assert result == "General support"


# Test synchronous MCP tool functions
def test_get_return_policy_no_category():
    """Test get_return_policy without specific category."""
    result = main.get_return_policy()

    assert "general_policy" in result
    assert "standard_return_window" in result["general_policy"]
    assert result["general_policy"]["standard_return_window"] == "30 days"
    assert "category_specific" not in result


def test_get_return_policy_electronics():
    """Test get_return_policy for electronics category."""
    result = main.get_return_policy("electronics")

    assert "general_policy" in result
    assert "category_specific" in result
    assert result["category_specific"]["return_window"] == "15 days"
    assert result["category_specific"]["restocking_fee"] == "10% for opened items"


def test_get_return_policy_clothing():
    """Test get_return_policy for clothing category."""
    result = main.get_return_policy("CLOTHING")  # Test case insensitive

    assert "general_policy" in result
    assert "category_specific" in result
    assert result["category_specific"]["return_window"] == "45 days"
    assert "size_exchange" in result["category_specific"]


def test_get_return_policy_unknown_category():
    """Test get_return_policy for unknown category."""
    result = main.get_return_policy("unknown")

    assert "general_policy" in result
    assert "category_specific" not in result


def test_get_shipping_info():
    """Test get_shipping_info function."""
    result = main.get_shipping_info()

    assert "domestic_options" in result
    assert "processing_time" in result
    assert result["domestic_options"]["standard_shipping"]["cost"] == "$5.99"
    assert result["domestic_options"]["free_shipping"]["threshold"] == 75.00


def test_get_contact_information():
    """Test get_contact_information function."""
    result = main.get_contact_information()

    assert "general_contact" in result
    assert "phone" in result["general_contact"]
    assert result["general_contact"]["phone"] == "1-800-SUPPORT (1-800-786-7678)"


def test_get_contact_information_with_params():
    """Test get_contact_information with parameters."""
    result = main.get_contact_information("billing", "urgent")

    assert "general_contact" in result
    assert "business_hours" in result["general_contact"]


def test_get_size_guide():
    """Test get_size_guide function."""
    result = main.get_size_guide("shirt", "nike")

    assert "measuring_instructions" in result
    assert "fitting_tips" in result
    assert "chest_bust" in result["measuring_instructions"]


def test_get_warranty_information_electronics():
    """Test get_warranty_information for electronics."""
    result = main.get_warranty_information("electronics", "2023-01-01")

    assert "warranty_terms" in result
    assert result["warranty_terms"]["standard_warranty"] == "1 year from purchase date"
    assert "Manufacturing defects" in result["warranty_terms"]["coverage"]


def test_get_warranty_information_clothing():
    """Test get_warranty_information for clothing."""
    result = main.get_warranty_information("clothing")

    assert "warranty_terms" in result
    assert result["warranty_terms"]["standard_warranty"] == "90 days quality guarantee"


def test_get_warranty_information_unknown():
    """Test get_warranty_information for unknown category."""
    result = main.get_warranty_information("unknown")

    assert result == {}


def test_get_payment_information():
    """Test get_payment_information function."""
    result = main.get_payment_information()

    assert "accepted_payments" in result
    assert "billing_information" in result
    assert "Visa" in result["accepted_payments"]["credit_cards"]["accepted"]
    assert "PayPal" in result["accepted_payments"]["digital_wallets"]["accepted"]


def test_get_payment_information_with_inquiry():
    """Test get_payment_information with inquiry type."""
    result = main.get_payment_information("billing")

    assert "accepted_payments" in result
    assert "when_charged" in result["billing_information"]


def test_get_account_help():
    """Test get_account_help function."""
    result = main.get_account_help("password_reset")

    assert "login_troubleshooting" in result
    assert "forgot_password" in result["login_troubleshooting"]
    assert "steps" in result["login_troubleshooting"]["forgot_password"]


def test_get_loyalty_program_info():
    """Test get_loyalty_program_info function."""
    result = main.get_loyalty_program_info()

    assert "program_overview" in result
    assert result["program_overview"]["name"] == "VIP Rewards Program"
    assert result["program_overview"]["earning_rate"] == "1 point per $1 spent"


def test_get_loyalty_program_info_with_inquiry():
    """Test get_loyalty_program_info with inquiry type."""
    result = main.get_loyalty_program_info("benefits")

    assert "program_overview" in result
    assert "redemption_rate" in result["program_overview"]


def test_get_product_care_info():
    """Test get_product_care_info function."""
    result = main.get_product_care_info("leather", "genuine")

    assert "general_tips" in result
    assert len(result["general_tips"]) > 0
    assert "Read care labels" in result["general_tips"][0]


@patch("os.path.exists")
def test_create_gradio_interface_with_gif(mock_exists):
    """Test create_gradio_interface when GIF file exists."""
    mock_exists.return_value = True

    demo = main.create_gradio_interface()
    assert demo is not None


@patch("os.path.exists")
def test_create_gradio_interface_without_gif(mock_exists):
    """Test create_gradio_interface when GIF file doesn't exist."""
    mock_exists.return_value = False

    demo = main.create_gradio_interface()
    assert demo is not None
