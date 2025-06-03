# 🛍️ MCP - Meta Commerce Platform - Universal E-commerce Customer Support Assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

**One Chat, Every Platform** - A platform-agnostic customer support assistant that
connects to any e-commerce system through pluggable strategies, using MCP (Model
Context Protocol) server and Gradio for the interface.

## 🎯 Features

- 📦 **Order Management**: Track orders, check status, view history
- 🔄 **Returns & Refunds**: Initiate returns, process refunds seamlessly
- ❌ **Cancellations**: Quick and easy order cancellations
- 💬 **Natural Language**: Conversational interface for customer support
- 🔌 **Platform Agnostic**: Extensible to any e-commerce platform
- 🚀 **Auto-Deploy**: Continuous deployment to Hugging Face Spaces

## 🏗️ Architecture

The system uses a Strategy Pattern to abstract different e-commerce platforms:

```ascii
┌─────────────────────────────────────────────────────────┐
│                    Gradio UI Layer                      │
│        (Customer Support Conversational Interface)      │
└─────────────────────────────┬───────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────┐
│                    MCP Server Core                      │
│  (Order Management, NLP Processing, Context Engine)     │
└─────────────────────────────┬───────────────────────────┘
                              │
┌─────────────────────────────▼───────────────────────────┐
│              E-commerce Strategy Interface              │
│   (MockData, Shopify, Magento, WooCommerce, etc.)       │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- Git
- Virtual environment tool (venv)

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/slavpilus/mcp.git
   cd mcp
   ```

2. **Run the setup script (macOS/Linux)**

   ```bash
   chmod +x scripts/setup_dev.sh
   ./scripts/setup_dev.sh
   ```

   Or manually:

   ```bash
   # Create virtual environment
   python -m venv venv

   # Activate virtual environment
   # On macOS/Linux:
   source venv/bin/activate
   # On Windows:
   venv\Scripts\activate

   # Install dependencies
   pip install -r requirements-dev.txt

   # Install pre-commit hooks
   pre-commit install
   ```

3. **Configure environment variables**

   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

4. **Run the application**

   ```bash
   python app.py
   ```

   The application will be available at `http://localhost:7860`

## 🛠️ Development

### Project Structure

```text
mcp/
├── .github/workflows/    # CI/CD pipelines
├── mcp_server/          # Core MCP server implementation
│   ├── strategies/      # E-commerce platform strategies
│   ├── models/          # Data models
│   └── utils/           # Utility functions
├── ui/                  # Gradio UI components
├── tests/               # Test suite
├── app.py               # Main Gradio application
└── requirements.txt     # Python dependencies
```

### Development Workflow

1. **Activate virtual environment**

   ```bash
   source venv/bin/activate  # macOS/Linux
   # or
   venv\Scripts\activate     # Windows
   ```

2. **Make your changes**
   - Follow the existing code style
   - Add tests for new functionality
   - Update documentation as needed

3. **Run code quality checks**

   ```bash
   # Format code
   black .
   isort .

   # Run linter
   ruff check .

   # Type checking
   mypy mcp_server ui
   ```

4. **Run tests**

   ```bash
   # Run all tests with coverage
   pytest

   # Run specific test file
   pytest tests/unit/test_strategies.py

   # Run with verbose output
   pytest -v
   ```

5. **Commit changes**

   ```bash
   git add .
   git commit -m "feat: your feature description"
   ```

   Pre-commit hooks will automatically run code quality checks.

### Code Style

This project uses:

- **Black** for code formatting (line length: 88)
- **isort** for import sorting
- **Ruff** for linting
- **MyPy** for type checking

All code must pass these checks before merging.

### Testing

- Minimum test coverage: 80%
- Write unit tests for all new functionality
- Integration tests for critical workflows
- Use pytest fixtures for test data

### Adding a New E-commerce Platform

1. Create a new strategy in `mcp_server/strategies/`:

   ```python
   from .base import EcommerceStrategy

   class YourPlatformStrategy(EcommerceStrategy):
       async def get_order(self, order_id: str) -> Optional[Order]:
           # Implementation here
           pass
   ```

2. Add tests in `tests/unit/test_your_platform_strategy.py`

3. Update the strategy factory to include your platform

## 📊 Environment Variables

Create a `.env` file based on `.env.example`:

```env
# Application Settings
DEBUG=False
LOG_LEVEL=INFO

# Hugging Face (for deployment)
HF_TOKEN=your_token_here
HF_USERNAME=your_username
HF_SPACE_NAME=your_space_name

# E-commerce Platforms (future)
# SHOPIFY_API_KEY=
# MAGENTO_API_URL=
```

## 🚀 Deployment

### Automatic Deployment

This project is configured for automatic deployment to Hugging Face Spaces:

1. Push to the `main` branch
2. GitHub Actions will run tests and quality checks
3. If all checks pass, the app deploys to Hugging Face Spaces

### Manual Deployment

To deploy manually to Hugging Face Spaces:

```bash
# Add Hugging Face remote
git remote add space https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

# Push to deploy
git push space main
```

## 🧪 Running Specific Commands

```bash
# Run only unit tests
pytest tests/unit/

# Run with coverage report
pytest --cov=mcp_server --cov=ui --cov-report=html

# Run linting
ruff check . --fix

# Format imports
isort .

# Type checking
mypy mcp_server ui --strict
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Commit Convention

We use conventional commits:

- `feat:` New features
- `fix:` Bug fixes
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.

## 🙏 Acknowledgments

- Built with [Gradio](https://gradio.app/)
- Uses [MCP (Model Context Protocol)](https://github.com/modelcontextprotocol)
- Deployed on [Hugging Face Spaces](https://huggingface.co/spaces)

## 📞 Support

For issues and feature requests, please use the
[GitHub Issues](https://github.com/slavpilus/mcp/issues) page.

---

**Status**: 🚧 Under active development - Phase 1: Core Foundation
