import os
import asyncio
import sys
from dotenv import load_dotenv

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.azure import AzureProvider
from pydantic_ai.mcp import MCPServerStdio

load_dotenv()

async def main():
    # --- 1. Setup Provider ---
    azure_provider = AzureProvider(
        azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
        api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        api_key=os.environ["AZURE_OPENAI_API_KEY"],
    )
    model = OpenAIChatModel(
        os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"], 
        provider=azure_provider
    )

    # --- 2. Define the Server Resource ---
    # We use 'uv run' to ensure the subprocess has all dependencies
    mcp_server = MCPServerStdio(
        'uv', 
        args=['run', 'mcp_server.py'],
        timeout=30.0 
    )

    # --- 3. Define the Agent ---
    # We pass the server instance into 'toolsets'.
    # The agent doesn't manage the server's life; it just uses it.
    agent = Agent(
        model=model,
        toolsets=[mcp_server],
        system_prompt=(
            "You are a helpful assistant. "
            "You MUST use the 'greet' tool for every greeting. "
            "Do not simply reply with text; execute the tool." 
            "You must reply exactly what the tool returns"
        )
    )

    # --- 4. Manual Lifecycle Management ---
    # This replaces 'agent.run_mcp_servers()'. 
    # We open the connection explicitly.
    print("Connecting to MCP Toolset...")
    async with mcp_server:
        print("Connected. Running agent...")
        
        # The agent sees the tools because the server context is active
        result = await agent.run("Please greet Adrian")
        
        print("\n=== FINAL OUTPUT ===")
        print(result.output)

        # Verification: Print tool usage
        print("\n=== TOOL USAGE LOG ===")
        for msg in result.all_messages():
            if hasattr(msg, 'parts'):
                for part in msg.parts:
                    if part.part_kind == 'tool-call':
                        print(f"✓ Tool Called: {part.tool_name} args={part.args}")
                    if part.part_kind == 'tool-return':
                        print(f"✓ Tool Returned: {part.content}")

if __name__ == "__main__":
    # Windows policy fix
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    
    asyncio.run(main())
