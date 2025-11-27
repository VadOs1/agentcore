import os
from bedrock_agentcore import BedrockAgentCoreApp
from dotenv import load_dotenv
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters
import asyncio


app = BedrockAgentCoreApp()

NAMING_SYSTEM_PROMPT = """
You are an assistant that helps Scrum Leaders by providing insights and information to facilitate their decisions.
You can search for information in Jira and GitHub.
"""

# Global variables for MCP client and agent
github_mcp_tools = None
naming_agent = None

async def initialize_mcp():
    """Initialize MCP client and agent"""
    global github_mcp_tools, naming_agent
    
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
    global naming_agent, github_mcp_tools
    
    # Initialize on first request if not already initialized
    if naming_agent is None:
        await initialize_mcp()
    
    user_message = payload.get("prompt", "Hi")
    
    # Run agent within MCP context
    async with github_mcp_tools:
        result = await naming_agent.run(user_message)
    
    return {"result": result}
    
if __name__ == '__main__':
    app.run()
        
