"""Test the main_stdio FastMCP server module (STDIO transport)."""

import pytest


def test_tools_registration():
    """Test that tools are properly registered with the MCP instance."""
    import main_stdio

    # Check that tools dictionary was created
    assert main_stdio.tools is not None
    assert isinstance(main_stdio.tools, dict)

    # Check that all expected tools are registered
    expected_tools = {
        "get_order_status",
        "cancel_order",
        "process_return",
        "track_package",
        "get_support_info",
    }
    assert set(main_stdio.tools.keys()) == expected_tools

    # Check that all tools are callable
    for tool_name, tool_func in main_stdio.tools.items():
        assert callable(tool_func), f"{tool_name} should be callable"


def test_mcp_server_initialization():
    """Test that the MCP server is properly initialized."""
    import main_stdio

    # Check that the FastMCP instance is created
    assert main_stdio.mcp is not None
    assert main_stdio.mcp.name == "Enneagora - E-commerce MCP Server"

    # Check that register_tools was called
    assert main_stdio.tools is not None


def test_stdio_logging_configuration():
    """Test that logging is configured properly for STDIO."""
    import logging

    import main_stdio

    # Check that logger exists
    assert main_stdio.logger is not None
    assert main_stdio.logger.name == "main_stdio"

    # Check that logging level is INFO
    assert main_stdio.logger.level <= logging.INFO


@pytest.mark.asyncio
async def test_tools_functionality():
    """Test that the registered tools actually work."""
    import main_stdio

    # Test get_order_status with a known pattern
    result = await main_stdio.tools["get_order_status"]("ORD-1001-S")
    assert "ORD-1001-S" in result
    assert "Status: Shipped" in result

    # Test cancel_order with a processing order
    result = await main_stdio.tools["cancel_order"]("ORD-1002-P")
    assert "ORD-1002-P" in result
    assert "cancelled" in result.lower()

    # Test track_package with a shipped order
    result = await main_stdio.tools["track_package"]("ORD-1003-T")
    assert "Tracking" in result
    assert "TRK" in result  # Should have tracking number

    # Test get_support_info
    result = await main_stdio.tools["get_support_info"]("returns")
    assert "return" in result.lower()


def test_same_tools_as_main():
    """Test that main_stdio has the same tools as main."""
    import main
    import main_stdio

    # Both should have the same tool names
    assert set(main.tools.keys()) == set(main_stdio.tools.keys())

    # Both should have the same number of tools
    assert len(main.tools) == len(main_stdio.tools)
