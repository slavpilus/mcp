#!/usr/bin/env python3
"""
Enneagora Interactive Hackathon Demo Script
Shows a live demo of the MCP server with actual LLM interactions using OpenAI
"""

import asyncio
import json
import os
import sys
import time
from pathlib import Path
from typing import Any

from openai import AsyncOpenAI

from mcp import ClientSession
from mcp.client.sse import sse_client


class DemoNarrator:
    """Handles the demo narrative with typing effects"""

    def __init__(self, typing_speed: float = 0.02):
        self.typing_speed = typing_speed

    def type_print(
        self, text: str, prefix: str = "", color: str = "", delay: float = None
    ):
        """Print text with typing effect"""
        if color:
            print(f"{color}{prefix}", end="", flush=True)
        else:
            print(prefix, end="", flush=True)

        for char in text:
            print(char, end="", flush=True)
            time.sleep(delay or self.typing_speed)

        if color:
            print("\033[0m")  # Reset color
        else:
            print()

    def instant_print(self, text: str, color: str = ""):
        """Print text instantly"""
        if color:
            print(f"{color}{text}\033[0m")
        else:
            print(text)


class MCPInteractiveDemoClient:
    """Interactive MCP client for demo purposes"""

    def __init__(self, openai_api_key: str):
        self.openai_client = AsyncOpenAI(api_key=openai_api_key)
        self.mcp_session = None
        self.available_tools = []
        self.narrator = DemoNarrator()

    async def connect_to_mcp_server(
        self, server_url: str = "http://localhost:7860/gradio_api/mcp/sse"
    ):
        """Connect to the MCP server via SSE and keep the connection open"""
        try:
            self.narrator.instant_print(
                f"🔌 Connecting to MCP server at {server_url}...", "\033[94m"
            )

            # Create a persistent connection
            self.sse_transport = sse_client(server_url)
            read, write = await self.sse_transport.__aenter__()

            self.client_session = ClientSession(read, write)
            session = await self.client_session.__aenter__()
            self.mcp_session = session

            # Initialize the session
            await session.initialize()
            self.narrator.instant_print("✅ MCP session initialized", "\033[92m")

            # List available tools
            tools_result = await session.list_tools()
            self.available_tools = tools_result.tools

            self.narrator.instant_print(
                f"🔧 Found {len(self.available_tools)} available tools:", "\033[92m"
            )
            for tool in self.available_tools:
                self.narrator.instant_print(
                    f"  • {tool.name}: {tool.description}", "\033[36m"
                )

            return session
        except Exception as e:
            self.narrator.instant_print(
                f"❌ Failed to connect to MCP server: {e}", "\033[91m"
            )
            self.narrator.instant_print(
                "💡 Make sure the Gradio MCP server is running at localhost:7860",
                "\033[93m",
            )
            return None

    async def close_connection(self):
        """Close the MCP connection"""
        try:
            if hasattr(self, "client_session"):
                await self.client_session.__aexit__(None, None, None)
            if hasattr(self, "sse_transport"):
                await self.sse_transport.__aexit__(None, None, None)
        except Exception as e:
            self.narrator.instant_print(f"⚠️ Error closing connection: {e}", "\033[93m")

    async def call_mcp_tool(self, tool_name: str, arguments: dict[str, Any]) -> str:
        """Call an MCP tool and return the result"""
        if not self.mcp_session:
            return "Error: Not connected to MCP server"

        try:
            self.narrator.instant_print(f"🔧 Calling MCP tool: {tool_name}", "\033[36m")
            self.narrator.instant_print(f"   Args: {arguments}", "\033[90m")

            result = await self.mcp_session.call_tool(tool_name, arguments)

            if result.content:
                response = (
                    result.content[0].text
                    if result.content[0].text
                    else str(result.content[0])
                )
                self.narrator.instant_print(f"   ✅ Response: {response}", "\033[90m")
                return response
            else:
                return "No response from tool"

        except Exception as e:
            error_msg = f"Error calling tool {tool_name}: {str(e)}"
            self.narrator.instant_print(f"   ❌ {error_msg}", "\033[91m")
            return error_msg

    def get_tools_for_openai(self) -> list:
        """Convert MCP tools to OpenAI function format"""
        openai_tools = []
        for tool in self.available_tools:
            # Get the input schema, with fallback for different attribute names
            input_schema = {"type": "object", "properties": {}}
            if hasattr(tool, "inputSchema") and tool.inputSchema:
                input_schema = tool.inputSchema
            elif hasattr(tool, "input_schema") and tool.input_schema:
                input_schema = tool.input_schema

            openai_tool = {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": input_schema,
                },
            }
            openai_tools.append(openai_tool)

            # Simplified tool registration logging
            # self.narrator.instant_print(f"   • {tool.name}", "\033[90m")

        return openai_tools

    async def get_ai_response(
        self, customer_message: str, scenario_context: str = ""
    ) -> tuple[str, list]:
        """Get AI response with potential tool calls"""
        try:
            system_prompt = f"""You are a helpful e-commerce customer support assistant with access to powerful MCP tools. You MUST use the available tools to provide accurate, real-time information.

Available context: {scenario_context}

CRITICAL INSTRUCTIONS - YOU MUST USE TOOLS:
- When a customer mentions an order number (like ORD-1001-D), IMMEDIATELY call get_order_status with the order_id parameter
- For tracking questions, call track_package tool after getting order status
- For return requests, call process_return tool with order details
- For product care questions, call get_product_care_info tool
- For loyalty/rewards questions, call get_loyalty_program_info tool
- For shipping address changes, call update_shipping_address tool
- For contact info requests, call get_contact_information tool

EXAMPLE - Customer asks about order ORD-1001-D:
1. FIRST call get_order_status(order_id="ORD-1001-D")
2. If tracking needed, call track_package(order_id="ORD-1001-D")
3. THEN respond with specific information from the tools

DO NOT provide generic responses or make up information. ALWAYS call the relevant MCP tools first to get accurate data, then provide a helpful response based on the tool results."""

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": customer_message},
            ]

            # Get OpenAI response with function calling
            tools = self.get_tools_for_openai()

            # Show tools being provided to AI
            if tools:
                self.narrator.instant_print(
                    f"🔧 Using {len(tools)} MCP tools for AI assistance", "\033[36m"
                )

            # For demo purposes, let's be more aggressive about requiring tool use
            tool_choice = "auto"
            if tools and any(
                keyword in customer_message.lower()
                for keyword in [
                    "order",
                    "ord-",
                    "track",
                    "return",
                    "loyalty",
                    "shipping",
                ]
            ):
                tool_choice = "required"
                self.narrator.instant_print(
                    "🎯 Requiring tool use for this query", "\033[93m"
                )

            response = await self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                tools=tools if tools else None,
                tool_choice=tool_choice if tools else None,
            )

            # Process the response
            assistant_message = response.choices[0].message
            tool_calls = []

            if assistant_message.tool_calls:
                self.narrator.instant_print(
                    f"✅ AI decided to use {len(assistant_message.tool_calls)} tools",
                    "\033[92m",
                )

                # Execute tool calls
                for tool_call in assistant_message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json.loads(tool_call.function.arguments)

                    # Call the MCP tool
                    tool_result = await self.call_mcp_tool(tool_name, tool_args)
                    tool_calls.append(
                        {"name": tool_name, "args": tool_args, "result": tool_result}
                    )

                # Get final response incorporating tool results
                messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_message.content,
                        "tool_calls": assistant_message.tool_calls,
                    }
                )

                for i, tool_call in enumerate(assistant_message.tool_calls):
                    messages.append(
                        {
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "content": tool_calls[i]["result"],
                        }
                    )

                final_response = await self.openai_client.chat.completions.create(
                    model="gpt-4", messages=messages
                )

                return final_response.choices[0].message.content, tool_calls
            else:
                if tools:
                    self.narrator.instant_print(
                        "⚠️ AI chose not to use any tools despite having access",
                        "\033[93m",
                    )
                return assistant_message.content, []

        except Exception as e:
            error_msg = f"Error getting AI response: {str(e)}"
            self.narrator.instant_print(f"❌ {error_msg}", "\033[91m")
            return (
                f"I apologize, but I'm having trouble processing your request right now. Error: {str(e)}",
                [],
            )


async def run_interactive_demo():
    """Main interactive demo sequence"""
    # Load environment variables
    env_path = Path(__file__).parent.parent / ".env"

    # Simple .env parser
    env_vars = {}
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_vars[key.strip()] = value.strip()

    openai_api_key = env_vars.get("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        print("❌ OPENAI_API_KEY not found in .env file or environment variables")
        print("Please set your OpenAI API key in the .env file")
        sys.exit(1)

    narrator = DemoNarrator()

    # Clear screen
    print("\033[2J\033[H")

    # Title
    narrator.instant_print("=" * 60, "\033[95m")
    narrator.instant_print(
        "    🏆 ENNEAGORA - INTERACTIVE MCP HACKATHON DEMO 🏆", "\033[95m"
    )
    narrator.instant_print(
        "      Live AI + MCP Integration for E-commerce Support", "\033[95m"
    )
    narrator.instant_print("=" * 60, "\033[95m")
    print()

    await asyncio.sleep(2)

    # Introduction
    narrator.type_print(
        "Welcome to the LIVE Enneagora demo with real AI interactions!",
        "📢 ",
        "\033[96m",
    )
    narrator.type_print(
        "This demo uses OpenAI GPT-4 with our MCP server for actual customer support.",
        "   ",
        "\033[96m",
    )
    print()
    await asyncio.sleep(1)

    # Initialize the interactive client
    client = MCPInteractiveDemoClient(openai_api_key)

    # Start MCP server connection
    print("\n" + "=" * 60)
    narrator.type_print("Starting MCP Connection", "🚀 ", "\033[93m", 0.05)
    print("=" * 60 + "\n")
    await asyncio.sleep(1)

    # Note about server status
    narrator.instant_print(
        "💡 This demo connects to your running Gradio MCP server:", "\033[93m"
    )
    narrator.instant_print(
        "   MCP Server endpoint: http://localhost:7860/gradio_api/mcp/sse", "\033[90m"
    )
    narrator.instant_print("   Gradio Interface: http://localhost:7860", "\033[90m")
    narrator.instant_print("", "")
    narrator.instant_print(
        "📋 Note: Make sure server is running with 'python main.py' before starting demo.",
        "\033[36m",
    )
    print()
    await asyncio.sleep(2)

    # Connect to MCP server once for the entire demo
    print("\n" + "=" * 60)
    narrator.type_print("LIVE CUSTOMER SUPPORT CONVERSATIONS", "💬 ", "\033[95m", 0.05)
    print("=" * 60 + "\n")

    # Connect to MCP server once at the beginning
    session = await client.connect_to_mcp_server()

    if not session:
        narrator.instant_print(
            "\n❌ DEMO FAILED: Could not connect to MCP server", "\033[91m"
        )
        narrator.instant_print(
            "\n💡 The MCP server may not be running or accessible via SSE:", "\033[93m"
        )
        narrator.instant_print("   1. Start the server: python main.py", "\033[93m")
        narrator.instant_print(
            "   2. Check if http://localhost:7860/gradio_api/mcp/sse is accessible",
            "\033[93m",
        )
        narrator.instant_print(
            "   3. Make sure Gradio server with mcp_server=True is running on port 7860",
            "\033[93m",
        )
        print()
        return  # Exit the demo

    # Demo scenarios with real AI interactions - key customer journeys
    scenarios = [
        {
            "title": "Frustrated Customer - Lost Package",
            "customer_message": "This is ridiculous! I ordered a birthday gift for my daughter THREE WEEKS AGO (order ORD-1001-D) and it's still not here. Her party is tomorrow and I'm absolutely furious. Where is my package?!",
            "context": "Customer is extremely frustrated about delayed order for time-sensitive gift.",
            "follow_up": "Thank you for looking into this. I found the package - it was delivered to my neighbor's house by mistake. I really appreciate your help and patience with my frustration.",
        },
        {
            "title": "Confused First-Time Customer",
            "customer_message": "Hi, I'm new to online shopping and I'm a bit confused. I ordered some clothes last week (ORD-1002-S) but I'm not sure how to track my order or what to do if they don't fit. Can you walk me through the whole process?",
            "context": "New customer needs guidance on order tracking and return process.",
            "follow_up": "That was so helpful! One more question - if I want to exchange the item for a different size instead of returning it, is that possible? And how long does the exchange usually take?",
        },
        {
            "title": "Bulk Order for Business",
            "customer_message": "Hello, I'm placing a large order for my company's corporate event. We need 50 polo shirts with our logo (order ORD-1004-B). I need to know about bulk discounts, customization timeline, and what happens if some shirts don't fit our employees properly.",
            "context": "Business customer with bulk order needs information about discounts, customization, and returns.",
            "follow_up": "Great information! We'd also like to add embroidered jackets to this order. Can you check if we can combine orders for better pricing? And do you offer size samples before we commit to the full order?",
        },
        {
            "title": "Loyal Customer Appreciation",
            "customer_message": "I've been shopping with you for over 5 years and I love your service! I just wanted to check on my recent order ORD-1005-P and also ask about your loyalty program. I've made dozens of purchases - are there any perks I should know about?",
            "context": "Long-term loyal customer checking order status and asking about loyalty benefits.",
            "follow_up": "Wow, I had no idea I had so many rewards points! How do I redeem them? And thank you for the surprise upgrade to express shipping - that's why I keep coming back to you!",
        },
    ]

    for i, scenario in enumerate(scenarios, 1):
        # Scenario header
        narrator.instant_print(
            f"\n📍 Live Scenario {i}: {scenario['title']}", "\033[93m"
        )
        print("-" * 50)
        await asyncio.sleep(1)

        # Customer message
        narrator.type_print(
            scenario["customer_message"], "🛍️ Customer: ", "\033[95m", 0.02
        )
        await asyncio.sleep(1)

        # Show AI thinking
        narrator.type_print(
            "Analyzing customer request and determining appropriate tools...",
            "🤔 AI: ",
            "\033[90m",
            0.01,
        )
        await asyncio.sleep(1)

        try:
            # Get AI response with tool usage using the existing MCP session
            ai_response, tool_calls = await client.get_ai_response(
                scenario["customer_message"], scenario["context"]
            )

            # Display tool calls if any
            if tool_calls:
                narrator.instant_print(
                    f"\n🔧 Tools used: {len(tool_calls)}", "\033[36m"
                )
                for tool_call in tool_calls:
                    narrator.instant_print(
                        f"   • {tool_call['name']}: {tool_call['args']}", "\033[90m"
                    )
                    narrator.instant_print(
                        f"     Result: {tool_call['result'][:100]}...", "\033[90m"
                    )

            # Display AI response
            narrator.type_print(ai_response, "\n🤖 AI Assistant: ", "\033[92m", 0.01)

            # Show follow-up interaction within the same session
            await asyncio.sleep(2)
            narrator.instant_print("\n💬 Follow-up conversation:", "\033[94m")
            narrator.type_print(scenario["follow_up"], "🛍️ Customer: ", "\033[95m", 0.02)
            await asyncio.sleep(1)

            # Get AI follow-up response
            followup_ai_response, followup_tool_calls = await client.get_ai_response(
                scenario["follow_up"],
                f"Follow-up to previous conversation about {scenario['context']}",
            )

            # Display follow-up tool calls if any
            if followup_tool_calls:
                narrator.instant_print(
                    f"\n🔧 Additional tools used: {len(followup_tool_calls)}",
                    "\033[36m",
                )
                for tool_call in followup_tool_calls:
                    narrator.instant_print(
                        f"   • {tool_call['name']}: {tool_call['args']}", "\033[90m"
                    )
                    narrator.instant_print(
                        f"     Result: {tool_call['result'][:100]}...", "\033[90m"
                    )

            # Display AI follow-up response
            narrator.type_print(
                followup_ai_response, "\n🤖 AI Assistant: ", "\033[92m", 0.01
            )

        except Exception as e:
            narrator.instant_print(
                f"❌ Error during conversation: {str(e)}", "\033[91m"
            )
            continue

        await asyncio.sleep(3)

    # Demo Summary
    print("\n\n" + "=" * 60)
    narrator.type_print("INTERACTIVE DEMO SUMMARY", "🎉 ", "\033[93m", 0.05)
    print("=" * 60)

    summary_points = [
        "✅ Live OpenAI GPT-4 integration with MCP tools",
        "✅ Real-time tool selection and execution",
        "✅ Natural conversation flow with follow-up interactions",
        "✅ Emotional intelligence and empathetic responses",
        "✅ Complex multi-step problem resolution",
        "✅ Seamless integration between AI reasoning and MCP actions",
        "✅ Production-ready customer support automation",
    ]

    for point in summary_points:
        narrator.instant_print(point, "\033[92m")
        await asyncio.sleep(0.5)

    print()
    narrator.type_print(
        "This demo showcases the true power of MCP + AI:", "🏆 ", "\033[95m", 0.03
    )
    narrator.type_print(
        "Real-time, intelligent, multi-turn customer conversations!",
        "   ",
        "\033[95m",
        0.03,
    )
    narrator.type_print(
        "From frustrated customers to loyal advocates - AI handles it all!",
        "   ",
        "\033[95m",
        0.03,
    )
    print()

    # Interactive demo stats
    narrator.instant_print("📊 Demo Statistics:", "\033[93m")
    narrator.instant_print(f"   • {len(scenarios)} key customer scenarios", "\033[36m")
    narrator.instant_print("   • 2-turn conversations with follow-ups", "\033[36m")
    narrator.instant_print(
        "   • 4 different customer types (frustrated, new, business, loyal)", "\033[36m"
    )
    narrator.instant_print("   • 14+ MCP tools demonstrated", "\033[36m")
    narrator.instant_print("   • Real-time AI decision making", "\033[36m")
    print()

    # Links
    narrator.instant_print(
        "🔗 Live Demo: https://huggingface.co/spaces/SlavPilus/mcp-for-commerce-platforms",
        "\033[36m",
    )
    narrator.instant_print("💻 GitHub: https://github.com/slavpilus/mcp", "\033[36m")
    narrator.instant_print(
        "🚀 Interactive Demo: Real AI + Real MCP + Real Customer Journeys", "\033[36m"
    )

    print("\n" + "=" * 60 + "\n")

    # Close MCP connection
    await client.close_connection()


if __name__ == "__main__":
    asyncio.run(run_interactive_demo())
