#!/bin/bash

# Enneagora Demo Recording Script
# Records the interactive demo using asciinema and converts to animated GIF

set -e  # Exit on any error

# Configuration
DEMO_NAME="enneagora-demo"
CAST_FILE="${DEMO_NAME}.cast"
GIF_FILE="${DEMO_NAME}.gif"
PROJECT_ROOT="$(dirname "$(dirname "$(realpath "$0")")")"
DEMO_SCRIPT="${PROJECT_ROOT}/demo/hackathon_demo_interactive.py"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🎬 Enneagora Demo Recording Script${NC}"
echo "=================================================="
echo

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install dependencies
install_dependencies() {
    echo -e "${YELLOW}📦 Checking dependencies...${NC}"

    # Check for asciinema
    if ! command_exists asciinema; then
        echo -e "${RED}❌ asciinema not found. Installing...${NC}"
        if command_exists pip; then
            pip install asciinema
        elif command_exists brew; then
            brew install asciinema
        else
            echo -e "${RED}❌ Cannot install asciinema. Please install manually:${NC}"
            echo "  pip install asciinema"
            echo "  or brew install asciinema"
            exit 1
        fi
    else
        echo -e "${GREEN}✅ asciinema found${NC}"
    fi

    # Check for agg (asciinema gif generator)
    if ! command_exists agg; then
        echo -e "${YELLOW}📦 Installing agg for GIF conversion...${NC}"
        if command_exists cargo; then
            cargo install --git https://github.com/asciinema/agg
        else
            echo -e "${YELLOW}⚠️  agg not found. Trying alternative installation...${NC}"
            # Try to download pre-built binary
            if [[ "$OSTYPE" == "darwin"* ]]; then
                echo -e "${YELLOW}📥 Downloading agg for macOS...${NC}"
                curl -L -o /tmp/agg https://github.com/asciinema/agg/releases/latest/download/agg-x86_64-apple-darwin
                chmod +x /tmp/agg
                sudo mv /tmp/agg /usr/local/bin/agg
            elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
                echo -e "${YELLOW}📥 Downloading agg for Linux...${NC}"
                curl -L -o /tmp/agg https://github.com/asciinema/agg/releases/latest/download/agg-x86_64-unknown-linux-musl
                chmod +x /tmp/agg
                sudo mv /tmp/agg /usr/local/bin/agg
            else
                echo -e "${RED}❌ Cannot install agg automatically. Please install manually:${NC}"
                echo "  cargo install --git https://github.com/asciinema/agg"
                echo -e "${YELLOW}⚠️  Continuing without GIF conversion...${NC}"
                SKIP_GIF=true
            fi
        fi
    else
        echo -e "${GREEN}✅ agg found${NC}"
    fi

    echo
}

# Function to check if MCP server is running
check_server() {
    echo -e "${YELLOW}🔍 Checking if MCP server is running...${NC}"

    if curl -s http://localhost:7860 >/dev/null 2>&1; then
        echo -e "${GREEN}✅ MCP server is running at http://localhost:7860${NC}"
    else
        echo -e "${RED}❌ MCP server not running!${NC}"
        echo -e "${YELLOW}Please start the server first:${NC}"
        echo "  cd ${PROJECT_ROOT}"
        echo "  python main.py"
        echo
        echo -e "${YELLOW}Then run this script again.${NC}"
        exit 1
    fi
    echo
}

# Function to setup terminal
setup_terminal() {
    echo -e "${YELLOW}🖥️  Setting up terminal for recording...${NC}"

    # Set terminal size for consistent recording
    if command_exists resize; then
        resize -s 35 120  # 35 rows, 120 columns
    fi

    # Clear terminal
    clear

    echo -e "${GREEN}✅ Terminal ready${NC}"
    echo
}

# Function to record demo
record_demo() {
    echo -e "${BLUE}🎬 Starting demo recording...${NC}"
    echo -e "${YELLOW}Press Ctrl+C when the demo completes to stop recording${NC}"
    echo

    # Change to project directory
    cd "$PROJECT_ROOT"

    # Start recording
    asciinema rec "$CAST_FILE" \
        --title "Enneagora - MCP E-commerce Demo" \
        --command "python demo/hackathon_demo_interactive.py" \
        --overwrite

    echo -e "${GREEN}✅ Recording saved to: ${CAST_FILE}${NC}"
    echo
}

# Function to convert to GIF
convert_to_gif() {
    if [[ "$SKIP_GIF" == "true" ]]; then
        echo -e "${YELLOW}⚠️  Skipping GIF conversion (agg not available)${NC}"
        return
    fi

    echo -e "${BLUE}🎨 Converting to animated GIF...${NC}"

    # Convert cast to GIF using agg
    agg "$CAST_FILE" "$GIF_FILE" \
        --font-size 14 \
        --line-height 1.2 \
        --cols 120 \
        --rows 35 \
        --theme monokai \
        --speed 1.0

    echo -e "${GREEN}✅ GIF created: ${GIF_FILE}${NC}"

    # Get file sizes
    CAST_SIZE=$(du -h "$CAST_FILE" | cut -f1)
    GIF_SIZE=$(du -h "$GIF_FILE" | cut -f1)

    echo -e "${BLUE}📊 File sizes:${NC}"
    echo "  Cast file: $CAST_SIZE"
    echo "  GIF file:  $GIF_SIZE"
    echo
}

# Function to display results
show_results() {
    echo -e "${GREEN}🎉 Recording complete!${NC}"
    echo "=================================================="
    echo
    echo -e "${BLUE}📁 Output files:${NC}"
    echo "  📼 Cast file: $(pwd)/$CAST_FILE"
    if [[ "$SKIP_GIF" != "true" ]]; then
        echo "  🎬 GIF file:  $(pwd)/$GIF_FILE"
    fi
    echo
    echo -e "${BLUE}🔗 Usage:${NC}"
    echo "  Play locally:     asciinema play $CAST_FILE"
    echo "  Share online:     asciinema upload $CAST_FILE"
    if [[ "$SKIP_GIF" != "true" ]]; then
        echo "  Use in README:    Include $GIF_FILE in your documentation"
    fi
    echo
}

# Main execution
main() {
    echo -e "${BLUE}Starting in project directory: ${PROJECT_ROOT}${NC}"
    echo

    # Install dependencies
    install_dependencies

    # Check if server is running
    check_server

    # Setup terminal
    setup_terminal

    # Give user a moment to prepare
    echo -e "${YELLOW}🚀 Ready to record! The demo will start automatically.${NC}"
    echo -e "${YELLOW}💡 The demo has built-in timing, so just let it run.${NC}"
    echo -e "${YELLOW}⏱️  Starting in 3 seconds...${NC}"
    sleep 3

    # Record the demo
    record_demo

    # Convert to GIF
    convert_to_gif

    # Show results
    show_results
}

# Handle Ctrl+C gracefully
trap 'echo -e "\n${YELLOW}Recording interrupted. Cleaning up...${NC}"; exit 1' INT

# Run main function
main "$@"
