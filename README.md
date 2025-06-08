---
title: Enneagora - E-commerce MCP Server
emoji: 🛍️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.33.0
app_file: app.py
pinned: false
license: mit
tags: ["mcp", "commerce", "customer support" ]
---

# Enneagora - E-commerce MCP Server

Enneagora is a Model Context Protocol (MCP) server providing AI-powered customer support tools for e-commerce platforms. This server can be integrated with Claude Desktop or any MCP-compatible client to handle customer inquiries about orders, returns, shipping, and general support.

## 🚀 Features

- **MCP-Compliant**: True MCP server implementation using FastMCP with SSE transport
- **5 Customer Support Tools**:
  - `get_order_status` - Check order status and details
  - `cancel_order` - Process order cancellations
  - `process_return` - Handle return requests
  - `track_package` - Track shipment status
  - `get_support_info` - Provide general support information
- **Platform Agnostic**: Strategy pattern for easy integration with any e-commerce platform
- **Production Ready**: CI/CD pipeline with automated deployment to Hugging Face Spaces

## 📋 Prerequisites

- Python 3.10 or higher
- pip package manager
- (Optional) Hugging Face account for deployment

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/slavpilus/enneagora.git
cd enneagora
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```


## 🚀 Running the Server

### Local Development (SSE Transport)

Run the MCP server locally with SSE transport (for web clients):

```bash
python main.py
```

The server will start on `http://localhost:7860` with the MCP endpoint at `http://localhost:7860/sse`.

### Local Development (STDIO Transport)

Run the MCP server with stdio transport (for Claude Desktop):

```bash
python main_stdio.py
```

This version communicates via standard input/output for Claude Desktop compatibility.

### Using with Claude Desktop

Claude Desktop currently supports only local MCP servers via stdio transport. To use Enneagora with Claude Desktop:

1. **Install dependencies** (if not already done):

```bash
cd /path/to/enneagora
python -m venv venv
./venv/bin/pip install -r requirements.txt  # On Windows: venv\Scripts\pip
```

2. **Configure Claude Desktop**:

**macOS/Linux** (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "enneagora": {
      "command": "/path/to/enneagora/bin/enneagora.sh"
    }
  }
}
```

**Windows** (`%APPDATA%\Claude\claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "enneagora": {
      "command": "C:\\path\\to\\enneagora\\bin\\enneagora.bat"
    }
  }
}
```

3. **Restart Claude Desktop** to load the MCP tools.

**Note**: The launcher scripts in the `bin/` directory automatically use the correct Python environment and stdio transport.

## 🧪 Testing the Tools

Once connected to Claude Desktop, you can use natural language to interact with the tools:

- "Check the status of order ORD-1001"
- "Cancel order ORD-1004"
- "I want to return my order ORD-1002"
- "Track my package"
- "What's your return policy?"

## 🏗️ Architecture

```ascii
┌─────────────────────────────────────┐
│         MCP Clients                 │
│  (Claude Desktop, Web Clients)      │
└──────────────┬──────────────────────┘
               │ SSE or STDIO Transport
┌──────────────▼──────────────────────┐
│      FastMCP Server                 │
│  • main.py (SSE for web/remote)     │
│  • main_stdio.py (STDIO for Claude) │
├─────────────────────────────────────┤
│  5 MCP Tools:                       │
│  • get_order_status(order_id)       │
│  • cancel_order(order_id, reason)   │
│  • process_return(order_id, items)  │
│  • track_package(order_id)          │
│  • get_support_info(topic)          │
├─────────────────────────────────────┤
│   E-commerce Strategy Layer         │
│  • Mock Strategy (Demo)             │
│  • Shopify Strategy (Future)        │
│  • Magento Strategy (Future)        │
└─────────────────────────────────────┘
```

## 🔧 Configuration

### Environment Variables

Currently, the server uses a mock data strategy for demonstration. In production, you would configure:

- `ECOMMERCE_PLATFORM`: E-commerce platform to use (e.g., "shopify", "magento")
- Platform-specific credentials (API keys, endpoints, etc.)

### Adding New E-commerce Platforms

1. Create a new strategy in `mcp_server/strategies/`:

```python
from .base import BaseEcommerceStrategy

class ShopifyStrategy(BaseEcommerceStrategy):
    def get_order_status(self, order_id: str) -> dict:
        # Implement Shopify API integration
        pass
```

2. Register the strategy in `mcp_server/strategies/__init__.py`

3. Configure the strategy in your environment

## 🚢 Deployment

### Deploy to Hugging Face Spaces

The SSE version can be deployed to Hugging Face Spaces for remote access:

1. Fork this repository
2. Set up GitHub secrets:
   - `HF_TOKEN`: Your Hugging Face token
   - `HF_USERNAME`: Your Hugging Face username
   - `HF_SPACE_NAME`: Name for your Space
   - `CODECOV_TOKEN`: (Optional) For code coverage reports
3. Push to main branch to trigger deployment

The deployed server will be available at:

- Web UI: `https://SlavPilus/mpc-for-commerce-platforms.hf.space/`
- SSE Endpoint: `https://SlavPilus/mpc-for-commerce-platforms.hf.space/sse`

### Manual Deployment

```bash
# Build Docker image
docker build -t enneagora .

# Run container
docker run -p 7860:7860 enneagora
```

**Note**: The Hugging Face deployment uses SSE transport and is accessible via HTTP. Claude Desktop cannot connect to remote SSE endpoints - use the local stdio version instead.

## 🧪 Development

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests with coverage
pytest --cov=enneagora --cov=main

# Run linting and formatting
black .
isort .
ruff check .
mypy enneagora main.py
```

### Project Structure

```text
enneagora/
├── main.py                 # FastMCP server (SSE transport)
├── main_stdio.py          # FastMCP server (STDIO transport for Claude Desktop)
├── bin/                   # Launcher scripts
│   ├── enneagora.sh       # Unix/macOS launcher
│   ├── enneagora.bat      # Windows batch launcher
│   └── enneagora.ps1      # Windows PowerShell launcher
├── mcp_server/            # Core server implementation
│   ├── server.py          # Main server logic
│   ├── models/            # Data models
│   └── strategies/        # E-commerce platform strategies
├── tests/                 # Test suite
├── scripts/               # Utility scripts
├── static/                # Web UI assets
│   └── index.html         # Server info page
└── requirements.txt       # Python dependencies
```

## 📝 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🐛 Troubleshooting

### Common Issues

1. **Claude Desktop doesn't see the tools**
   - Verify the server is running and accessible
   - Check the MCP endpoint URL in Claude Desktop config
   - Restart Claude Desktop after configuration changes

2. **Server connection issues**
   - Ensure the server is running on the correct port
   - Check firewall settings for local development
   - Verify the SSE endpoint is accessible

## 📚 Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/jlowin/fastmcp)
- [Hugging Face Spaces](https://huggingface.co/spaces)

## 🏆 Acknowledgments

Enneagora was built for the Hugging Face MCP Hackathon, demonstrating the power of Model Context Protocol for creating AI-powered customer support systems.
