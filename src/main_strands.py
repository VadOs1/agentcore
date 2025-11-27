import os
from bedrock_agentcore import BedrockAgentCoreApp
from dotenv import load_dotenv
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters


app = BedrockAgentCoreApp()

@app.entrypoint
async def start(payload):

    user_message = payload.get("prompt", "Hi")

    result = naming_agent(user_message)
        
    return {"result": result}
    
if __name__ == '__main__':
    NAMING_SYSTEM_PROMPT = """
    You are an assistant that helps Scrum Leaders by providing insights and information to facilitate their decisions.
    You can search for information in Jira and GitHub.
    """

    # print("Initializing Atlassian MCP tools (this may take a moment)...")
    # atlassian_tools = MCPClient(
    #     lambda: stdio_client(
    #         StdioServerParameters(
    #             command="npx",
    #             args=[
    #                 "-y",
    #                 "mcp-remote",
    #                 "https://mcp.atlassian.com/v1/sse",
    #                 "--transport",
    #                 "sse-only",
    #             ],
    #             env={
    #                 **dict(os.environ),
    #                 "ATLASSIAN_API_TOKEN": os.environ.get("ATLASSIAN_API_TOKEN"),
    #                 "ATLASSIAN_EMAIL": os.environ.get("ATLASSIAN_EMAIL"),
    #             },
    #         )
    #     ),
    #     startup_timeout=60,
    # )

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

    with github_mcp_tools:#, atlassian_tools:
        #atlassian_tool_list = atlassian_tools.list_tools_sync()
        github_tool_list = github_mcp_tools.list_tools_sync()
        tools = github_tool_list # + atlassian_tool_list
        print(
            f"✓ Loaded {len(github_tool_list)} GitHub tools"
        )

        naming_agent = Agent(
            system_prompt=NAMING_SYSTEM_PROMPT,
            model=os.environ.get("anthropic.claude-sonnet-4-20250514-v1:0"),
            tools=tools,
        )
        
    app.run()
        
