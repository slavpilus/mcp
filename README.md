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
git clone https://github.com/yourusername/enneagora.git
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

### Local Development

Run the MCP server locally:

```bash
python main.py
```

The server will start on `http://localhost:8000` with the MCP endpoint at `http://localhost:8000/sse`.

### Using with Claude Desktop

1. Add the server to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "ecommerce": {
      "url": "http://localhost:8000/sse"
    }
  }
}
```

2. For a deployed server on Hugging Face Spaces:

```json
{
  "mcpServers": {
    "ecommerce": {
      "url": "https://SlavPilus.hf.space/enneagora/sse"
    }
  }
}
```

3. Restart Claude Desktop to load the MCP tools.

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
│  (Claude Desktop, Other Clients)    │
└──────────────┬──────────────────────┘
               │ SSE Transport
┌──────────────▼──────────────────────┐
│      FastMCP Server (main.py)       │
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

1. Fork this repository
2. Set up GitHub secrets:
   - `HF_TOKEN`: Your Hugging Face token
   - `HF_USERNAME`: Your Hugging Face username
   - `HF_SPACE_NAME`: Name for your Space
3. Push to main branch to trigger deployment

### Manual Deployment

```bash
# Build Docker image
docker build -t enneagora

# Run container
docker run -p 8000:8000 enneagora
```

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
├── main.py                 # FastMCP server entry point
├── mcp_server/            # Core server implementation
│   ├── server.py          # Main server logic
│   ├── nlp_processor.py   # NLP processing layer
│   ├── models/            # Data models
│   └── strategies/        # E-commerce platform strategies
├── tests/                 # Test suite
├── scripts/               # Utility scripts
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

Enneagora was built for the MCP Hackathon, demonstrating the power of Model Context Protocol for creating AI-powered customer support systems.
