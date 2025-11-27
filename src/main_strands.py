import os
from bedrock_agentcore import BedrockAgentCoreApp
from dotenv import load_dotenv
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters


app = BedrockAgentCoreApp()

NAMING_SYSTEM_PROMPT = """
You are an assistant that helps Scrum Leaders by providing insights and information to facilitate their decisions.
You can search for information in Jira and GitHub.
"""

# Initialize MCP client globally
print("Initializing GitHub MCP tools (this may take a moment)...")
github_mcp_tools = MCPClient(
    lambda: stdio_client(
        StdioServerParameters(
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"],
            env={
                **dict(os.environ),
                "GITHUB_PERSONAL_ACCESS_TOKEN": os.environ.get("GITHUB_TOKEN"),
            },
        )
    ),
    startup_timeout=30,
)

# Start MCP context
github_mcp_tools.__enter__()
github_tool_list = github_mcp_tools.list_tools_sync()
print(f"✓ Loaded {len(github_tool_list)} GitHub tools")

# Create agent with MCP tools
naming_agent = Agent(
    system_prompt=NAMING_SYSTEM_PROMPT,
    model="anthropic.claude-sonnet-4-20250514-v1:0",
    tools=github_tool_list,
)

@app.entrypoint
async def start(payload):
    user_message = payload.get("prompt", "Hi")
    result = await naming_agent.run(user_message)
    return {"result": result}
    
if __name__ == '__main__':
    try:
        app.run()
    finally:
        # Clean up MCP client on exit
        github_mcp_tools.__exit__(None, None, None)
        
