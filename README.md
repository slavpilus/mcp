---
title: Enneagora - E-commerce MCP Server
emoji: 🛍️
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 5.33.0
app_file: main.py
pinned: false
license: mit
tags: ["mcp", "commerce", "customer support" ]
---

# Enneagora - E-commerce MCP Server

Enneagora is a Universal E-commerce Customer Support Assistant using the Model Context Protocol (MCP) that provides a platform-agnostic solution for customer support across different e-commerce platforms. This comprehensive MCP server can be integrated with Claude Desktop or any MCP-compatible client to handle all aspects of customer inquiries.

## 🚀 Features

- **MCP-Compliant**: True MCP server implementation using FastMCP with both SSE and STDIO transports
- **14 Comprehensive Customer Support Tools**:
  - **Order Management**: `get_order_status`, `cancel_order`, `process_return`, `track_package`
  - **Support Information**: `get_support_info`, `get_return_policy`, `get_shipping_info`, `get_contact_information`
  - **Product Guidance**: `get_size_guide`, `get_warranty_information`, `get_product_care_info`
  - **Account & Payment**: `get_payment_information`, `get_account_help`, `get_loyalty_program_info`
- **Platform Agnostic**: Strategy pattern for easy integration with any e-commerce platform
- **Dynamic Mock Data**: Intelligent test data system with pattern-based order behavior
- **Dual Transport Support**: SSE for web/remote clients, STDIO for Claude Desktop
- **Production Ready**: CI/CD pipeline with automated deployment to Hugging Face Spaces

## 📋 Prerequisites

- Python 3.10 or higher
- pip package manager
- (Optional) Hugging Face account for deployment

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/slavpilus/mcp.git
cd mcp
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

## 🚀 Usage Options

### Option 1: Remote SSE Integration (Recommended for Web Apps)

Use the hosted Hugging Face Spaces endpoint for immediate access:

**SSE Endpoint:** `https://huggingface.co/spaces/SlavPilus/mpc-for-commerce-platforms/sse`

**Advantages:**
- No local setup required
- Always up-to-date with latest features
- Scalable for multiple clients
- Perfect for web applications and API integrations

### Option 2: Local Development & Claude Desktop

#### Local SSE Server (for web/remote clients)

```bash
python main.py
```

The server starts on `http://localhost:7860` with MCP endpoint at `http://localhost:7860/sse`.

#### Claude Desktop Integration (STDIO)

**Step 1: Configure Claude Desktop**

**macOS:** Edit `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows:** Edit `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "enneagora": {
      "command": "python",
      "args": ["/full/absolute/path/to/mcp/main_stdio.py"],
      "env": {}
    }
  }
}
```

**⚠️ Important:**
- Use the full absolute path to `main_stdio.py`
- Ensure your Python environment has all dependencies installed
- Restart Claude Desktop after configuration changes

**Step 2: Test Configuration**

You can test the STDIO version manually:
```bash
python main_stdio.py
```

## 🔧 All Available Tools

### Order Management Tools
1. **get_order_status** - Get detailed order status and tracking information
2. **cancel_order** - Cancel orders with validation checks
3. **process_return** - Handle return requests with prepaid labels
4. **track_package** - Track package delivery with real-time updates

### Information & Support Tools
5. **get_support_info** - General support information and guidance
6. **get_return_policy** - Detailed return policies by product category
7. **get_shipping_info** - Shipping rates, delivery times, and international options
8. **get_contact_information** - Contact details by issue type and urgency

### Product & Service Tools
9. **get_size_guide** - Size charts for clothing, shoes, and accessories
10. **get_warranty_information** - Warranty coverage and claims processing
11. **get_product_care_info** - Care instructions and maintenance guidance

### Account & Payment Tools
12. **get_payment_information** - Payment methods, billing help, and troubleshooting
13. **get_account_help** - Account troubleshooting and login assistance
14. **get_loyalty_program_info** - Rewards program details and member benefits

## 🧪 Testing with Dynamic Mock Data

Enneagora features an intelligent mock data system where order behavior is determined by ID patterns:

### Order Status Patterns
- `ORD-XXXX-D` - Delivered orders (e.g., ORD-1001-D)
- `ORD-XXXX-S` - Shipped orders with tracking (e.g., ORD-1002-S)
- `ORD-XXXX-T` - In Transit with location updates (e.g., ORD-1003-T)
- `ORD-XXXX-P` - Processing orders (e.g., ORD-1004-P)
- `ORD-XXXX-R` - Ready for Pickup (e.g., ORD-1005-R)
- `ORD-XXXX-C` - Cancelled orders (e.g., ORD-1006-C)
- `ORD-XXXX-F` - Failed/Problem orders (e.g., ORD-1007-F)
- `ORD-XXXX-E` - Error/Not Found (e.g., ORD-1008-E)
- `ORD-XXXX` - Pending orders (no suffix, e.g., ORD-1009)

### Example Queries

Once connected to Claude Desktop or an MCP client, you can use natural language:

**Order Management:**
- "Check the status of order ORD-1001-S"
- "Cancel order ORD-1004-P because I found a better price"
- "I want to return my order ORD-1002-D, it didn't fit properly"

**Product Information:**
- "What's your return policy for electronics?"
- "How much does shipping cost to Canada for a $45 order?"
- "What's the size guide for men's shirts?"
- "Is my laptop still under warranty? I bought it on 2023-06-15"

**Account & Payment:**
- "My credit card was declined, what should I do?"
- "I forgot my password, how can I reset it?"
- "How does your loyalty program work?"

**Product Care:**
- "How do I care for my silk dress?"
- "What's the best way to clean leather shoes?"

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
│  14 MCP Tools:                      │
│  • Order Management (4 tools)       │
│  • Information & Support (4 tools)  │
│  • Product & Service (3 tools)      │
│  • Account & Payment (3 tools)      │
├─────────────────────────────────────┤
│   E-commerce Strategy Layer         │
│  • Mock Strategy (Demo/Testing)     │
│  • Shopify Strategy (Future)        │
│  • Magento Strategy (Future)        │
│  • WooCommerce Strategy (Future)    │
└─────────────────────────────────────┘
```

## 🚢 Deployment

### Hosted on Hugging Face Spaces

The server is deployed and accessible at:
- **Web UI:** https://huggingface.co/spaces/SlavPilus/mpc-for-commerce-platforms
- **SSE Endpoint:** https://huggingface.co/spaces/SlavPilus/mpc-for-commerce-platforms/sse

### Manual Deployment

```bash
# Build Docker image
docker build -t enneagora .

# Run container
docker run -p 7860:7860 enneagora
```

### Deploy Your Own Instance

1. Fork this repository
2. Set up GitHub secrets:
   - `HF_TOKEN`: Your Hugging Face token
   - `HF_USERNAME`: Your Hugging Face username
   - `HF_SPACE_NAME`: Name for your Space
3. Push to main branch to trigger deployment

## 🧪 Development

### Running Tests

```bash
# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests with coverage
pytest --cov=mcp_server --cov=main

# Run linting and formatting
pre-commit run --all-files
```

### Project Structure

```text
mcp/
├── main.py                 # FastMCP server (SSE transport)
├── main_stdio.py          # FastMCP server (STDIO transport for Claude Desktop)
├── mcp_server/            # Core server implementation
│   ├── server.py          # Main server logic
│   ├── mcp_tools.py       # All 14 MCP tool definitions
│   └── strategies/        # E-commerce platform strategies
│       ├── base.py        # Base strategy interface
│       └── mock_strategy.py # Mock data strategy
├── tests/                 # Comprehensive test suite
│   ├── unit/              # Unit tests (96%+ coverage)
│   └── integration/       # Integration tests
├── static/                # Web UI assets
│   └── index.html         # Server info and documentation page
├── requirements.txt       # Python dependencies
├── requirements-dev.txt   # Development dependencies
└── pyproject.toml         # Project configuration
```

## 🔧 Configuration

### Environment Variables

Currently uses mock data for demonstration. In production, configure:

- `ECOMMERCE_PLATFORM`: Platform to use (e.g., "shopify", "magento")
- Platform-specific credentials (API keys, endpoints, etc.)

### Adding New E-commerce Platforms

1. Create a new strategy in `mcp_server/strategies/`:

```python
from .base import EcommerceStrategy

class ShopifyStrategy(EcommerceStrategy):
    async def get_order(self, order_id: str):
        # Implement Shopify API integration
        pass
```

2. Register the strategy in your configuration
3. Configure credentials and endpoints

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
   - Verify the configuration file path and syntax
   - Ensure you're using the full absolute path to `main_stdio.py`
   - Check that Python environment has all dependencies
   - Restart Claude Desktop after configuration changes

2. **Server connection issues**
   - Ensure the server is running on the correct port
   - Check firewall settings for local development
   - Verify the SSE endpoint is accessible

3. **Import errors or missing dependencies**
   - Activate your virtual environment
   - Run `pip install -r requirements.txt`
   - Ensure Python 3.10+ is installed

### Testing Configuration

Test your local setup:
```bash
# Test STDIO version
python main_stdio.py

# Test SSE version
python main.py
# Then visit http://localhost:7860
```

## 📚 Resources

- **Project Repository:** [https://github.com/slavpilus/mcp](https://github.com/slavpilus/mcp)
- **MCP Documentation:** [Model Context Protocol](https://modelcontextprotocol.io/)
- **FastMCP Documentation:** [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- **Hugging Face Spaces:** [HF Spaces Documentation](https://huggingface.co/docs/hub/spaces)

## 🏆 Acknowledgments

Enneagora was built to demonstrate the power of Model Context Protocol for creating comprehensive AI-powered customer support systems as part of the Hugging Face MCP Hackathon. It showcases how MCP can bridge the gap between AI assistants and real-world e-commerce operations.

**Key Features Demonstrated:**
- Comprehensive tool ecosystem (14 interconnected tools)
- Dynamic mock data with intelligent behavior patterns
- Multi-transport support (SSE + STDIO)
- Production-ready deployment and CI/CD
- Type-safe implementation with 96%+ test coverage
