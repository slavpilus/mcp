"""
Enneagora - MCP Server for E-commerce Customer Support

This runs a Gradio interface with built-in MCP server functionality.
The MCP server provides 14 comprehensive e-commerce customer support tools.
"""

import logging
from pathlib import Path

import gradio as gr

from mcp_server.server import EcommerceMCPServer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the e-commerce server instance
ecommerce_server = EcommerceMCPServer()


# Define standalone functions for Gradio MCP auto-discovery
async def get_order_status(order_id: str, customer_id: str = "default") -> str:
    """Get status for a specific order."""
    return await ecommerce_server.get_order_status(order_id, customer_id)


async def cancel_order(
    order_id: str, reason: str = "Customer requested", customer_id: str = "default"
) -> str:
    """Cancel an order."""
    return await ecommerce_server.cancel_order(order_id, reason, customer_id)


async def process_return(
    order_id: str,
    item_ids_str: str = "",
    reason: str = "Customer return",
    customer_id: str = "default",
) -> str:
    """Process a return request for an order."""
    # Convert string to list for the server call
    item_ids = (
        None
        if not item_ids_str.strip()
        else [item.strip() for item in item_ids_str.split(",")]
    )
    return await ecommerce_server.process_return(
        order_id, item_ids, reason, customer_id
    )


async def track_package(order_id: str, customer_id: str = "default") -> str:
    """Track package delivery status for an order."""
    return await ecommerce_server.track_package(order_id, "order", customer_id)


async def get_support_info(topic: str = "general", customer_id: str = "default") -> str:
    """Get customer support information for a specific topic."""
    return await ecommerce_server.get_support_info(topic, customer_id)


def get_return_policy(product_category: str | None = None) -> dict:
    """Get comprehensive return and refund policy information."""
    # Implementation from mcp_tools.py
    base_policy = {
        "standard_return_window": "30 days",
        "condition_requirements": [
            "Items must be unused and in original condition",
            "Original packaging and tags must be included",
            "Receipt or order confirmation required",
        ],
        "refund_timeframe": "3-5 business days after we receive returned item",
        "return_shipping": "Free prepaid return labels provided",
        "restocking_fee": "None for standard items",
    }

    category_specific = {
        "electronics": {
            "return_window": "15 days",
            "special_conditions": [
                "Software must be unopened",
                "Original accessories required",
            ],
            "restocking_fee": "10% for opened items",
        },
        "clothing": {
            "return_window": "45 days",
            "special_conditions": [
                "Must not show signs of wear",
                "Hygiene items non-returnable",
            ],
            "size_exchange": "Free size exchanges within 60 days",
        },
    }

    result = {"general_policy": base_policy}
    if product_category and product_category.lower() in category_specific:
        result["category_specific"] = category_specific[product_category.lower()]

    return result


def get_shipping_info(
    destination_country: str | None = None, order_value: float | None = None
) -> dict:
    """Get shipping options, costs, and delivery timeframes."""
    return {
        "domestic_options": {
            "standard_shipping": {"cost": "$5.99", "timeframe": "5-7 business days"},
            "expedited_shipping": {"cost": "$12.99", "timeframe": "2-3 business days"},
            "overnight_shipping": {"cost": "$24.99", "timeframe": "Next business day"},
            "free_shipping": {
                "threshold": 75.00,
                "conditions": "Standard shipping on orders $75+",
            },
        },
        "processing_time": "1-2 business days before shipment",
    }


def get_contact_information(
    issue_type: str | None = None, urgency: str | None = "normal"
) -> dict:
    """Get customer service contact information."""
    return {
        "general_contact": {
            "phone": "1-800-SUPPORT (1-800-786-7678)",
            "email": "support@example.com",
            "live_chat": "Available on website 24/7",
            "business_hours": {
                "phone_support": "Monday-Friday 8 AM - 8 PM EST",
                "email_response": "Within 24 hours on business days",
            },
        }
    }


def get_size_guide(product_type: str, brand: str | None = None) -> dict:
    """Get size guide information for clothing, shoes, and accessories."""
    return {
        "measuring_instructions": {
            "chest_bust": "Measure around the fullest part of chest/bust",
            "waist": "Measure around natural waistline",
            "hips": "Measure around fullest part of hips",
        },
        "fitting_tips": [
            "When between sizes, size up for comfort",
            "Check fabric content - stretchy materials may fit differently",
        ],
    }


def get_warranty_information(
    product_category: str, purchase_date: str | None = None
) -> dict:
    """Get warranty and guarantee information for products."""
    warranty_terms = {
        "electronics": {
            "standard_warranty": "1 year from purchase date",
            "coverage": ["Manufacturing defects", "Hardware failures"],
        },
        "clothing": {
            "standard_warranty": "90 days quality guarantee",
            "coverage": ["Seam failures", "Zipper defects"],
        },
    }

    result = {}
    if product_category.lower() in warranty_terms:
        result["warranty_terms"] = warranty_terms[product_category.lower()]

    return result


def get_payment_information(inquiry_type: str | None = None) -> dict:
    """Get information about accepted payment methods and billing."""
    return {
        "accepted_payments": {
            "credit_cards": {
                "accepted": ["Visa", "Mastercard", "American Express", "Discover"]
            },
            "digital_wallets": {"accepted": ["PayPal", "Apple Pay", "Google Pay"]},
        },
        "billing_information": {
            "when_charged": {
                "authorization": "When order is placed",
                "capture": "When item ships",
            },
        },
    }


def get_account_help(issue_type: str) -> dict:
    """Get help with account-related issues and login problems."""
    return {
        "login_troubleshooting": {
            "forgot_password": {
                "steps": [
                    "Click 'Forgot Password' on login page",
                    "Enter email address associated with account",
                    "Check email for reset link",
                    "Follow link to create new password",
                ]
            }
        }
    }


def get_loyalty_program_info(inquiry_type: str | None = None) -> dict:
    """Get information about loyalty program, rewards, and member benefits."""
    return {
        "program_overview": {
            "name": "VIP Rewards Program",
            "enrollment": "Free to join, automatic with first purchase",
            "earning_rate": "1 point per $1 spent",
            "redemption_rate": "100 points = $5 reward",
        }
    }


def get_product_care_info(product_category: str, material: str | None = None) -> dict:
    """Get care instructions and maintenance information for products."""
    return {
        "general_tips": [
            "Read care labels before cleaning any item",
            "Test cleaning products on inconspicuous area first",
            "Address stains and damage promptly for best results",
        ]
    }


# Count available tools
TOOLS = [
    get_order_status,
    cancel_order,
    process_return,
    track_package,
    get_support_info,
    get_return_policy,
    get_shipping_info,
    get_contact_information,
    get_size_guide,
    get_warranty_information,
    get_payment_information,
    get_account_help,
    get_loyalty_program_info,
    get_product_care_info,
]
logger.info(f"Loaded {len(TOOLS)} MCP tools for Gradio auto-discovery")


def create_gradio_interface() -> gr.Blocks:
    """Create the Gradio interface that displays hackathon submission content."""

    html_file = Path(__file__).parent / "static" / "index.html"

    try:
        full_html = html_file.read_text()
        # Extract content between <body> tags since Gradio strips HTML/head/body
        import re

        body_match = re.search(r"<body[^>]*>(.*?)</body>", full_html, re.DOTALL)
        if body_match:
            html_content = body_match.group(1)
        else:
            html_content = full_html
        logger.info("Loaded hackathon submission HTML content from index.html")
    except FileNotFoundError:
        logger.warning("Static HTML file not found, using fallback content")
        html_content = f"""
        <div class="hackathon-header">
            <h1>🏆 Enneagora - MCP Hackathon Submission</h1>
            <p class="subtitle">Universal E-commerce Customer Support Assistant using Model Context Protocol</p>
            <div class="badges">
                <span class="badge">🥇 MCP Tool/Server Track</span>
                <span class="badge">🛠️ 14 Comprehensive Tools</span>
                <span class="badge">🚀 Production Ready</span>
                <span class="badge">✅ 96% Test Coverage</span>
            </div>
        </div>

        <div class="container">
            <div class="hackathon-info">
                <h2>🎯 Hackathon Submission Details</h2>
                <div class="stats">
                    <div class="stat">
                        <span class="stat-number">14</span>
                        <span>MCP Tools</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">96%</span>
                        <span>Test Coverage</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">128</span>
                        <span>Unit Tests</span>
                    </div>
                    <div class="stat">
                        <span class="stat-number">2</span>
                        <span>Transport Protocols</span>
                    </div>
                </div>
                <p><strong>Track:</strong> MCP Tool/Server Track</p>
                <p><strong>Innovation Focus:</strong> First comprehensive e-commerce customer support MCP server</p>
                <p><strong>Technical Excellence:</strong> Type-safe implementation, comprehensive testing, dual MCP server support</p>
            </div>

            <h1>🛒 Enneagora - E-commerce MCP Server</h1>
            <p>
                <span class="status">🔴 Live Server</span>
                Universal MCP-compliant server for e-commerce customer support with {len(TOOLS)} comprehensive tools
            </p>

            <div class="success">
                <h3>🎯 Gradio MCP Integration</h3>
                <p><strong>Server Type:</strong> Native Gradio MCP Server</p>
                <p><strong>Protocol:</strong> MCP (Model Context Protocol)</p>
                <p><strong>Tools Available:</strong> {len(TOOLS)} comprehensive e-commerce support tools</p>
                <p><strong>MCP Endpoint:</strong> <code>http://localhost:7860/gradio_api/mcp/sse</code></p>
                <p><strong>Compatibility:</strong> All MCP-compatible clients and applications</p>
            </div>
        </div>
        """

    demo: gr.Blocks
    with gr.Blocks(
        title="Enneagora - MCP Hackathon Submission",
        theme=gr.themes.Default(primary_hue="blue", secondary_hue="gray"),
        css="""
        /* Force light theme - override dark mode */
        :root {
            --color-accent: #2563eb !important;
            --color-accent-soft: #dbeafe !important;
            --background-fill-primary: white !important;
            --background-fill-secondary: #f8fafc !important;
            --color-text-label: #374151 !important;
            --color-text-display: #1f2937 !important;
            --block-background-fill: white !important;
            --block-border-color: #e5e7eb !important;
            --button-primary-background-fill: #2563eb !important;
            --button-primary-text-color: white !important;
        }

        /* Hide theme switcher/toggle and settings links */
        .theme-toggle,
        .theme-switch,
        button[aria-label*="theme"],
        button[aria-label*="Theme"],
        .dark-mode-toggle,
        [data-testid="theme-toggle"],
        /* Hide settings/preferences links that lead to theme options */
        a[href*="settings"],
        a[href*="preferences"],
        button[aria-label*="settings"],
        button[aria-label*="Settings"],
        .settings-link,
        .footer a,
        .gradio-footer a,
        .footer-links a,
        [data-testid="settings-button"],
        .svelte-1ax1toq a,
        .footer .svelte-1ax1toq {
            display: none !important;
            visibility: hidden !important;
        }

        /* Hide entire footer if it only contains settings */
        .footer:has(a[href*="settings"]),
        .gradio-footer:has(a),
        footer:has(a[href*="settings"]),
        /* Additional Gradio footer selectors */
        .gradio-container footer,
        .gradio-container .footer,
        div[class*="footer"],
        .svelte-1ax1toq:has(a),
        .app > div:last-child:has(a[href*="settings"]) {
            display: none !important;
        }

        /* Hide any remaining footer links generically */
        .gradio-container a[target="_blank"]:not([href*="huggingface"]):not([href*="github"]) {
            display: none !important;
        }

        /* Override font face declarations to prevent 404 errors */
        @font-face {
            font-family: 'ui-sans-serif';
            src: local('system-ui'), local('-apple-system'), local('BlinkMacSystemFont');
        }
        @font-face {
            font-family: 'system-ui';
            src: local('system-ui'), local('-apple-system'), local('BlinkMacSystemFont');
        }

        /* Reset and base styles - Mobile first */
        .gradio-container {
            max-width: 1200px !important;
            margin: 0 auto !important;
            padding: 0.5rem !important;
            background: white !important;
        }

        @media (min-width: 768px) {
            .gradio-container {
                padding: 0 !important;
            }
        }

        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
            min-height: 100vh !important;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
            line-height: 1.6 !important;
            color: #333 !important;
        }

        /* Ensure all content areas use light theme */
        .gradio-container, .gradio-container * {
            color-scheme: light !important;
        }

        /* Hackathon header styles */
        .hackathon-header {
            background: linear-gradient(135deg, #FF6B6B, #FF8E53) !important;
            color: white !important;
            padding: 2rem !important;
            border-radius: 12px !important;
            margin-bottom: 2rem !important;
            text-align: center !important;
        }

        .hackathon-header h1 {
            margin: 0 0 0.5rem 0 !important;
            font-size: 2.5rem !important;
            font-weight: bold !important;
            color: white !important;
        }

        .hackathon-header .subtitle {
            font-size: 1.2rem !important;
            opacity: 0.9 !important;
            margin: 0 !important;
        }

        /* Badges */
        .badges {
            display: flex !important;
            gap: 1rem !important;
            margin: 1.5rem 0 !important;
            flex-wrap: wrap !important;
            justify-content: center !important;
        }

        .badge {
            background: rgba(255,255,255,0.2) !important;
            padding: 0.5rem 1rem !important;
            border-radius: 20px !important;
            font-weight: 500 !important;
            backdrop-filter: blur(10px) !important;
        }

        /* Container styles */
        .container {
            background-color: white !important;
            padding: 2.5rem !important;
            border-radius: 12px !important;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1) !important;
            margin-bottom: 2rem !important;
        }

        /* Typography */
        h1 {
            color: #2563eb !important;
            border-bottom: 2px solid #e5e7eb !important;
            padding-bottom: 0.5rem !important;
        }

        h2 {
            color: #1f2937 !important;
            margin-top: 2.5rem !important;
            font-size: 1.8rem !important;
        }

        h3 {
            color: #374151 !important;
            margin-top: 1.5rem !important;
            font-size: 1.3rem !important;
        }

        /* Status badge */
        .status {
            display: inline-block !important;
            padding: 0.5rem 1rem !important;
            background-color: #10b981 !important;
            color: white !important;
            border-radius: 25px !important;
            font-size: 0.9rem !important;
            font-weight: 600 !important;
            text-transform: uppercase !important;
            letter-spacing: 0.5px !important;
        }

        /* Info sections */
        .hackathon-info {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: white !important;
            padding: 2rem !important;
            border-radius: 12px !important;
            margin: 2rem 0 !important;
        }

        .hackathon-info h2 {
            color: white !important;
            margin-top: 0 !important;
        }

        .success {
            background-color: #f0f9ff !important;
            border: 2px solid #60a5fa !important;
            border-radius: 8px !important;
            padding: 1.5rem !important;
            margin: 1.5rem 0 !important;
        }

        .success h3 {
            color: #2563eb !important;
            margin-top: 0 !important;
        }

        /* Stats grid */
        .stats {
            display: grid !important;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)) !important;
            gap: 1rem !important;
            margin: 1.5rem 0 !important;
        }

        .stat {
            text-align: center !important;
            padding: 1rem !important;
            background: rgba(255,255,255,0.1) !important;
            border-radius: 8px !important;
        }

        .stat-number {
            font-size: 2rem !important;
            font-weight: bold !important;
            display: block !important;
        }

        /* Code styling */
        code {
            background-color: #e5e7eb !important;
            padding: 0.2rem 0.4rem !important;
            border-radius: 3px !important;
            font-size: 0.9em !important;
            color: #1f2937 !important;
        }

        /* Tools and feature grids */
        .tools-grid, .feature-grid {
            display: grid !important;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)) !important;
            gap: 1.5rem !important;
            margin: 1.5rem 0 !important;
        }

        .tool, .feature-card {
            background-color: #f8fafc !important;
            padding: 1.2rem !important;
            border-radius: 8px !important;
            margin-bottom: 1rem !important;
            border-left: 4px solid #3b82f6 !important;
            transition: transform 0.2s ease !important;
        }

        .tool:hover, .feature-card:hover {
            transform: translateX(4px) !important;
        }

        .tool h3, .feature-card h3 {
            margin: 0 0 0.5rem 0 !important;
            color: #1e40af !important;
        }

        /* Demo section */
        .demo-section {
            background: linear-gradient(135deg, #FF6B6B, #FF8E53) !important;
            color: white !important;
            padding: 2rem !important;
            border-radius: 12px !important;
            margin: 2rem 0 !important;
        }

        .demo-section h2 {
            color: white !important;
            margin-top: 0 !important;
        }

        /* CTA Buttons */
        .cta-button {
            display: inline-block !important;
            background: white !important;
            color: #2563eb !important;
            padding: 1rem 2rem !important;
            border-radius: 8px !important;
            text-decoration: none !important;
            font-weight: 600 !important;
            margin: 1rem 0.5rem 0 0 !important;
            transition: transform 0.2s ease !important;
        }

        .cta-button:hover {
            transform: translateY(-2px) !important;
        }

        /* Integration sections */
        .integration-section {
            background-color: #f8fafc !important;
            border: 2px solid #e2e8f0 !important;
            border-radius: 12px !important;
            padding: 2rem !important;
            margin: 1.5rem 0 !important;
        }

        .url-box {
            background: linear-gradient(135deg, #fef3c7, #fcd34d) !important;
            border: 2px solid #f59e0b !important;
            border-radius: 8px !important;
            padding: 1.5rem !important;
            margin: 1.5rem 0 !important;
        }

        .warning {
            background-color: #fef2f2 !important;
            border: 2px solid #fca5a5 !important;
            border-radius: 8px !important;
            padding: 1.5rem !important;
            margin: 1.5rem 0 !important;
        }

        /* Highlight sections */
        .highlight-section {
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: white !important;
            padding: 2rem !important;
            border-radius: 12px !important;
            margin: 2rem 0 !important;
        }

        .highlight-section h2 {
            color: white !important;
            margin-top: 0 !important;
        }

        /* Video placeholder */
        .video-placeholder {
            background: rgba(255,255,255,0.2) !important;
            border: 2px dashed rgba(255,255,255,0.5) !important;
            padding: 3rem !important;
            text-align: center !important;
            border-radius: 8px !important;
            margin: 1rem 0 !important;
        }

        /* Pre code blocks */
        pre {
            background-color: #1f2937 !important;
            color: #f3f4f6 !important;
            padding: 1.5rem !important;
            border-radius: 8px !important;
            overflow-x: auto !important;
            border: 1px solid #374151 !important;
        }
        """,
    ) as demo:

        # Display the hackathon submission content
        gr.HTML(value=html_content)

        # Add JavaScript to suppress console errors and enforce light theme
        # Note: Demo GIF now served from external URL to comply with HF restrictions

        gr.HTML(
            """
            <script>
            // Force light theme and hide theme toggles
            function forceLightTheme() {
                // Remove dark theme classes
                document.documentElement.classList.remove('dark');
                document.body.classList.remove('dark');

                // Set light theme attributes
                document.documentElement.setAttribute('data-theme', 'light');
                document.documentElement.style.colorScheme = 'light';

                // Hide any theme toggle buttons and settings links
                const elementsToHide = document.querySelectorAll(
                    '.theme-toggle, .theme-switch, [data-testid="theme-toggle"], ' +
                    'button[aria-label*="theme"], button[aria-label*="Theme"], ' +
                    '.dark-mode-toggle, button[title*="theme"], button[title*="Theme"], ' +
                    // Settings and footer links
                    'a[href*="settings"], a[href*="preferences"], ' +
                    'button[aria-label*="settings"], button[aria-label*="Settings"], ' +
                    '.settings-link, .footer a, .gradio-footer a, ' +
                    '[data-testid="settings-button"], .footer-links a, ' +
                    '.svelte-1ax1toq a, .footer .svelte-1ax1toq'
                );
                elementsToHide.forEach(element => {
                    element.style.display = 'none';
                    element.style.visibility = 'hidden';
                });

                // Also hide footer containers that only have settings links
                const footers = document.querySelectorAll('.footer, .gradio-footer, footer');
                footers.forEach(footer => {
                    const links = footer.querySelectorAll('a');
                    const hasOnlySettings = Array.from(links).every(link =>
                        link.href && (link.href.includes('settings') || link.href.includes('preferences'))
                    );
                    if (hasOnlySettings && links.length > 0) {
                        footer.style.display = 'none';
                    }
                });
            }

            // Apply light theme immediately and on DOM changes
            forceLightTheme();

            // Watch for DOM changes to catch dynamically added theme toggles
            const observer = new MutationObserver(forceLightTheme);
            observer.observe(document.body, { childList: true, subtree: true });

            // Suppress postMessage errors
            window.addEventListener('error', function(e) {
                if (e.message.includes('postMessage') || e.message.includes('origin')) {
                    e.preventDefault();
                    return false;
                }
            });

            // Override console.error to filter font-related errors
            const originalError = console.error;
            console.error = function(...args) {
                const message = args.join(' ');
                if (message.includes('ui-sans-serif') ||
                    message.includes('system-ui') ||
                    message.includes('woff2') ||
                    message.includes('postMessage') ||
                    message.includes('target origin')) {
                    return; // Suppress these specific errors
                }
                originalError.apply(console, args);
            };

            setTimeout(function() {
                // Force light theme again after components load
                forceLightTheme();
            }, 1000);
            </script>
            """
        )

        # Hidden interfaces for MCP tool discovery (not visible to users)
        with gr.Tab("🔧 MCP Tools (Hidden)", visible=False):
            gr.Interface(
                fn=get_order_status,
                inputs=[gr.Textbox(), gr.Textbox()],
                outputs=gr.Textbox(),
            )
            gr.Interface(
                fn=cancel_order,
                inputs=[gr.Textbox(), gr.Textbox(), gr.Textbox()],
                outputs=gr.Textbox(),
            )
            gr.Interface(
                fn=process_return,
                inputs=[gr.Textbox(), gr.Textbox(), gr.Textbox(), gr.Textbox()],
                outputs=gr.Textbox(),
            )
            gr.Interface(
                fn=track_package,
                inputs=[gr.Textbox(), gr.Textbox()],
                outputs=gr.Textbox(),
            )
            gr.Interface(
                fn=get_support_info,
                inputs=[gr.Textbox(), gr.Textbox()],
                outputs=gr.Textbox(),
            )
            gr.Interface(
                fn=get_contact_information,
                inputs=[gr.Textbox(), gr.Textbox()],
                outputs=gr.JSON(),
            )
            gr.Interface(fn=get_return_policy, inputs=[gr.Textbox()], outputs=gr.JSON())
            gr.Interface(
                fn=get_shipping_info,
                inputs=[gr.Textbox(), gr.Number()],
                outputs=gr.JSON(),
            )
            gr.Interface(
                fn=get_size_guide,
                inputs=[gr.Textbox(), gr.Textbox()],
                outputs=gr.JSON(),
            )
            gr.Interface(
                fn=get_warranty_information,
                inputs=[gr.Textbox(), gr.Textbox()],
                outputs=gr.JSON(),
            )
            gr.Interface(
                fn=get_payment_information, inputs=[gr.Textbox()], outputs=gr.JSON()
            )
            gr.Interface(fn=get_account_help, inputs=[gr.Textbox()], outputs=gr.JSON())
            gr.Interface(
                fn=get_loyalty_program_info, inputs=[gr.Textbox()], outputs=gr.JSON()
            )
            gr.Interface(
                fn=get_product_care_info,
                inputs=[gr.Textbox(), gr.Textbox()],
                outputs=gr.JSON(),
            )

    return demo


if __name__ == "__main__":
    logger.info("Starting Enneagora - Gradio MCP Server")

    # Set up static file serving
    import os

    # Create and launch Gradio interface with MCP server
    demo = create_gradio_interface()

    # Set up static file serving
    project_root = os.path.dirname(__file__)
    static_dir = os.path.join(project_root, "static")

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        quiet=False,
        mcp_server=True,  # Enable built-in MCP server
        allowed_paths=[project_root, static_dir],  # Allow serving from root and static
        favicon_path=None,  # Disable favicon loading
        app_kwargs={
            "docs_url": None,  # Disable docs endpoint
            "redoc_url": None,  # Disable redoc endpoint
        },
    )
