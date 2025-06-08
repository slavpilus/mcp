# Enneagora MCP Server launcher for Windows PowerShell
# This script runs the MCP server with stdio transport for Claude Desktop

# Get the directory where this script is located
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$projectRoot = Split-Path -Parent $scriptDir

# Change to the project directory
Set-Location $projectRoot

# Check if virtual environment exists
if (-not (Test-Path "venv")) {
    Write-Error "Virtual environment not found at $projectRoot\venv"
    Write-Error "Please run 'python -m venv venv' and '.\venv\Scripts\pip install -r requirements.txt' first"
    exit 1
}

# Use the virtual environment's Python directly
& "$projectRoot\venv\Scripts\python.exe" "$projectRoot\main_stdio.py"
