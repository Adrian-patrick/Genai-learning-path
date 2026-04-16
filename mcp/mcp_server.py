from fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name: str) -> str:
    """Greets a user by name."""
    # We add a unique signature so you know it came from the tool
    return f"Greetings from the MCP Core, {name}!"

if __name__ == "__main__":
    mcp.run()
