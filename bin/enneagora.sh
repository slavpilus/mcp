#!/bin/bash
# Enneagora MCP Server launcher for Unix/macOS
# This script runs the MCP server with stdio transport for Claude Desktop

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/.." && pwd )"

# Change to the project directory
cd "$PROJECT_ROOT"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Error: Virtual environment not found at $PROJECT_ROOT/venv" >&2
    echo "Please run 'python -m venv venv && ./venv/bin/pip install -r requirements.txt' first" >&2
    exit 1
fi

# Use the virtual environment's Python directly
exec "$PROJECT_ROOT/venv/bin/python" "$PROJECT_ROOT/main_stdio.py"
