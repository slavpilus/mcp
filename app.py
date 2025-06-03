from datetime import datetime

import gradio as gr
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Version info for tracking deployments
VERSION = "0.1.0"
DEPLOY_TIME = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")


def process_message(message: str, history: list) -> tuple[str, list]:
    """Process user message and return response."""
    # Placeholder implementation
    response = f"Echo: {message} (v{VERSION})"
    history.append([message, response])
    return "", history


def create_app() -> gr.Blocks:
    """Create and configure the Gradio application."""
    with gr.Blocks(
        title="E-commerce Support Assistant",
        theme=gr.themes.Soft(),
    ) as app:
        gr.Markdown(
            f"""
            # Universal E-commerce Support Assistant

            **Version**: {VERSION} | **Deployed**: {DEPLOY_TIME}

            Welcome! I can help you with:
            - Order tracking and status
            - Returns and refunds
            - Order cancellations
            - Order history
            - General inquiries

            **Status**: Under Construction - Core foundation being built
            """
        )

        with gr.Row():
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    value=[["Assistant", "Hello! How can I help you today?"]],
                    height=500,
                    bubble_full_width=False,
                )

                with gr.Row():
                    msg = gr.Textbox(
                        label="Your message",
                        placeholder="Ask about your orders...",
                        lines=1,
                        scale=4,
                    )
                    submit = gr.Button("Send", variant="primary", scale=1)

                with gr.Row():
                    clear = gr.Button("Clear Chat")
                    gr.Examples(
                        examples=[
                            "Where is my order #12345?",
                            "I want to return my last order",
                            "Show me all my recent orders",
                            "What's your return policy?",
                        ],
                        inputs=msg,
                    )

            with gr.Column(scale=1):
                gr.Markdown("### Order Summary")
                gr.Markdown("*No order selected*")

                gr.Markdown("### Quick Actions")
                gr.Radio(
                    choices=[
                        "Track Order",
                        "Start Return",
                        "Cancel Order",
                        "Contact Support",
                    ],
                    label="What would you like to do?",
                )

        # Event handlers
        msg.submit(process_message, [msg, chatbot], [msg, chatbot])
        submit.click(process_message, [msg, chatbot], [msg, chatbot])
        clear.click(lambda: [[], ""], outputs=[chatbot, msg])

        gr.Markdown(
            """
            ---
            <center>
            <small>
            Powered by MCP (Model Context Protocol) |
            <a href="https://github.com/YOUR_USERNAME/ecommerce-support-mcp"
               target="_blank">GitHub</a> |
            Auto-deployed via GitHub Actions
            </small>
            </center>
            """
        )

    return app


# Create the app instance
demo = create_app()

if __name__ == "__main__":
    # Run locally
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
    )
