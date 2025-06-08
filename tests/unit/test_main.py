"""Test the main FastMCP server module (SSE transport)."""

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


def test_tools_registration():
    """Test that tools are properly registered with the MCP instance."""
    # Check that tools dictionary was created
    assert main.tools is not None
    assert isinstance(main.tools, dict)

    # Check that all expected tools are registered
    expected_tools = {
        "get_order_status",
        "cancel_order",
        "process_return",
        "track_package",
        "get_support_info",
    }
    assert set(main.tools.keys()) == expected_tools

    # Check that all tools are callable
    for tool_name, tool_func in main.tools.items():
        assert callable(tool_func), f"{tool_name} should be callable"


def test_mcp_server_initialization():
    """Test that the MCP server is properly initialized."""
    # Check that the FastMCP instance is created
    assert main.mcp is not None
    assert main.mcp.name == "Enneagora - E-commerce MCP Server"

    # Check that register_tools was called
    assert main.tools is not None
