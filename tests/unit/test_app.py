"""Tests for the Gradio app module."""
import sys
from unittest import mock


def test_app_module_structure():
    """Test that app.py has the expected structure."""
    # Mock the modules that cause import issues
    sys.modules["gradio"] = mock.MagicMock()
    sys.modules["dotenv"] = mock.MagicMock()

    # Import app module
    import app

    # Test that required functions exist
    assert hasattr(app, "process_message")
    assert hasattr(app, "create_app")
    assert hasattr(app, "demo")
    assert hasattr(app, "VERSION")
    assert hasattr(app, "DEPLOY_TIME")

    # Clean up
    del sys.modules["app"]
    del sys.modules["gradio"]
    del sys.modules["dotenv"]


def test_process_message_logic():
    """Test the process_message function logic."""
    # Mock gradio
    sys.modules["gradio"] = mock.MagicMock()
    sys.modules["dotenv"] = mock.MagicMock()

    import app

    # Test process_message
    history = []
    new_msg, new_history = app.process_message("Hello", history)

    assert new_msg == ""  # Message box should be cleared
    assert len(new_history) == 1
    assert new_history[0][0] == "Hello"
    assert "Echo: Hello" in new_history[0][1]
    assert app.VERSION in new_history[0][1]

    # Clean up
    del sys.modules["app"]
    del sys.modules["gradio"]
    del sys.modules["dotenv"]


def test_create_app_returns_blocks():
    """Test that create_app returns a Gradio Blocks instance."""
    # Create mock Gradio module
    mock_gradio = mock.MagicMock()
    mock_blocks = mock.MagicMock()
    mock_blocks.title = "E-commerce Support Assistant"
    mock_gradio.Blocks.return_value.__enter__.return_value = mock_blocks

    sys.modules["gradio"] = mock_gradio
    sys.modules["dotenv"] = mock.MagicMock()

    import app

    # Test create_app
    result = app.create_app()

    # Verify Blocks was called with correct parameters
    mock_gradio.Blocks.assert_called_with(
        title="E-commerce Support Assistant", theme=mock_gradio.themes.Soft()
    )

    assert result == mock_blocks

    # Clean up
    del sys.modules["app"]
    del sys.modules["gradio"]
    del sys.modules["dotenv"]


def test_app_constants():
    """Test that app constants are properly defined."""
    sys.modules["gradio"] = mock.MagicMock()
    sys.modules["dotenv"] = mock.MagicMock()

    import app

    # Test VERSION
    assert isinstance(app.VERSION, str)
    assert app.VERSION == "0.1.0"

    # Test DEPLOY_TIME
    assert isinstance(app.DEPLOY_TIME, str)
    assert "UTC" in app.DEPLOY_TIME

    # Clean up
    del sys.modules["app"]
    del sys.modules["gradio"]
    del sys.modules["dotenv"]
