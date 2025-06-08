@echo off
REM Enneagora MCP Server launcher for Windows
REM This script runs the MCP server with stdio transport for Claude Desktop

REM Get the directory where this script is located
set "SCRIPT_DIR=%~dp0"
REM Remove trailing backslash
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"
REM Get the project root (parent directory)
for %%I in ("%SCRIPT_DIR%") do set "PROJECT_ROOT=%%~dpI"
REM Remove trailing backslash
set "PROJECT_ROOT=%PROJECT_ROOT:~0,-1%"

REM Change to the project directory
cd /d "%PROJECT_ROOT%"

REM Check if virtual environment exists
if not exist "venv" (
    echo Error: Virtual environment not found at %PROJECT_ROOT%\venv >&2
    echo Please run 'python -m venv venv' and 'venv\Scripts\pip install -r requirements.txt' first >&2
    exit /b 1
)

REM Use the virtual environment's Python directly
"%PROJECT_ROOT%\venv\Scripts\python.exe" "%PROJECT_ROOT%\main_stdio.py"
