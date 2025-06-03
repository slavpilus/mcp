#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[*]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

# Header
echo -e "${BLUE}=================================================${NC}"
echo -e "${BLUE}🚀 MCP Development Environment Setup${NC}"
echo -e "${BLUE}=================================================${NC}"
echo ""

# Check Python version
print_status "Checking Python version..."
python_version=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
required_version="3.10"

if [[ $(echo "$python_version >= $required_version" | bc) -eq 1 ]]; then
    print_success "Python $python_version found (>= $required_version required)"
else
    print_error "Python $python_version found. Python >= $required_version required"
    exit 1
fi

# Create virtual environment
print_status "Creating virtual environment..."
if [ -d "venv" ]; then
    print_warning "Virtual environment already exists. Skipping creation."
else
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        print_success "Virtual environment created"
    else
        print_error "Failed to create virtual environment"
        exit 1
    fi
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate
if [ $? -eq 0 ]; then
    print_success "Virtual environment activated"
else
    print_error "Failed to activate virtual environment"
    exit 1
fi

# Upgrade pip
print_status "Upgrading pip..."
pip install --upgrade pip --quiet
if [ $? -eq 0 ]; then
    print_success "pip upgraded"
else
    print_error "Failed to upgrade pip"
    exit 1
fi

# Install dependencies
print_status "Installing production dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt --quiet
    if [ $? -eq 0 ]; then
        print_success "Production dependencies installed"
    else
        print_error "Failed to install production dependencies"
        exit 1
    fi
else
    print_warning "requirements.txt not found. Skipping production dependencies."
fi

print_status "Installing development dependencies..."
if [ -f "requirements-dev.txt" ]; then
    pip install -r requirements-dev.txt --quiet
    if [ $? -eq 0 ]; then
        print_success "Development dependencies installed"
    else
        print_error "Failed to install development dependencies"
        exit 1
    fi
else
    print_warning "requirements-dev.txt not found. Skipping development dependencies."
fi

# Install pre-commit hooks
print_status "Installing pre-commit hooks..."
# First, ensure pre-commit is in PATH by using the venv's python
if [ -f "venv/bin/pre-commit" ] || [ -f "venv/Scripts/pre-commit.exe" ]; then
    # Use the pre-commit from virtual environment
    if [ -f "venv/bin/pre-commit" ]; then
        venv/bin/pre-commit install
    else
        venv/Scripts/pre-commit.exe install
    fi
    if [ $? -eq 0 ]; then
        print_success "Pre-commit hooks installed"
    else
        print_error "Failed to install pre-commit hooks"
    fi
elif python -m pre_commit --version &> /dev/null; then
    # Try using pre-commit as a module
    python -m pre_commit install
    if [ $? -eq 0 ]; then
        print_success "Pre-commit hooks installed"
    else
        print_error "Failed to install pre-commit hooks"
    fi
else
    print_warning "pre-commit not found. Make sure requirements-dev.txt includes pre-commit."
    print_warning "You can install hooks later with: pre-commit install"
fi

# Create .env file if it doesn't exist
print_status "Setting up environment variables..."
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    print_success ".env file created from .env.example"
    print_warning "Please edit .env and add your configuration values"
elif [ -f ".env" ]; then
    print_success ".env file already exists"
else
    print_warning ".env.example not found. Please create .env manually"
fi

# Run initial code quality checks (optional)
print_status "Running initial code quality checks..."
echo ""

# Check if tools are available and run them
# Use tools from virtual environment
BLACK_CMD=""
ISORT_CMD=""
RUFF_CMD=""

if [ -f "venv/bin/black" ]; then
    BLACK_CMD="venv/bin/black"
elif [ -f "venv/Scripts/black.exe" ]; then
    BLACK_CMD="venv/Scripts/black.exe"
elif python -m black --version &> /dev/null; then
    BLACK_CMD="python -m black"
fi

if [ -f "venv/bin/isort" ]; then
    ISORT_CMD="venv/bin/isort"
elif [ -f "venv/Scripts/isort.exe" ]; then
    ISORT_CMD="venv/Scripts/isort.exe"
elif python -m isort --version &> /dev/null; then
    ISORT_CMD="python -m isort"
fi

if [ -f "venv/bin/ruff" ]; then
    RUFF_CMD="venv/bin/ruff"
elif [ -f "venv/Scripts/ruff.exe" ]; then
    RUFF_CMD="venv/Scripts/ruff.exe"
elif python -m ruff --version &> /dev/null; then
    RUFF_CMD="python -m ruff"
fi

if [ -n "$BLACK_CMD" ]; then
    print_status "Running Black formatter..."
    $BLACK_CMD . --check --quiet
    if [ $? -eq 0 ]; then
        print_success "Code is properly formatted"
    else
        print_warning "Some files need formatting. Run 'black .' to fix"
    fi
fi

if [ -n "$ISORT_CMD" ]; then
    print_status "Running isort..."
    $ISORT_CMD . --check-only --quiet
    if [ $? -eq 0 ]; then
        print_success "Imports are properly sorted"
    else
        print_warning "Some imports need sorting. Run 'isort .' to fix"
    fi
fi

if [ -n "$RUFF_CMD" ]; then
    print_status "Running Ruff linter..."
    $RUFF_CMD check . --quiet
    if [ $? -eq 0 ]; then
        print_success "No linting issues found"
    else
        print_warning "Some linting issues found. Run 'ruff check . --fix' to fix"
    fi
fi

# Summary
echo ""
echo -e "${GREEN}=================================================${NC}"
echo -e "${GREEN}✅ Development environment setup complete!${NC}"
echo -e "${GREEN}=================================================${NC}"
echo ""
echo -e "${YELLOW}📍 Current status:${NC}"
echo -e "  • Virtual environment: ${GREEN}Activated${NC}"
echo -e "  • Dependencies: ${GREEN}Installed${NC}"
echo -e "  • Pre-commit hooks: ${GREEN}Configured${NC}"
echo ""
echo -e "${YELLOW}📝 Next steps:${NC}"
echo -e "  1. Configure your environment:"
echo -e "     ${BLUE}edit .env${NC} (add your Hugging Face tokens, etc.)"
echo ""
echo -e "  2. Run tests to verify setup:"
echo -e "     ${BLUE}pytest${NC}"
echo ""
echo -e "  3. Start the application:"
echo -e "     ${BLUE}python app.py${NC}"
echo ""
echo -e "  4. Before committing code:"
echo -e "     ${BLUE}black . && isort . && ruff check .${NC}"
echo ""
echo -e "${YELLOW}💡 Tips:${NC}"
echo -e "  • To deactivate the virtual environment: ${BLUE}deactivate${NC}"
echo -e "  • To reactivate later: ${BLUE}source venv/bin/activate${NC}"
echo -e "  • View test coverage: ${BLUE}pytest --cov-report=html${NC}"
echo ""
echo -e "${GREEN}Happy coding! 🎉${NC}"
