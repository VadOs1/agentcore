import os
from bedrock_agentcore import BedrockAgentCoreApp
from strands import Agent
from strands.tools.mcp import MCPClient
from mcp import stdio_client, StdioServerParameters


app = BedrockAgentCoreApp()

NAMING_SYSTEM_PROMPT = """
You are an expert in GitHub and you can check any Pull Request and provide valuable feedback.
"""


@app.entrypoint
def start(payload):
    user_message = payload.get(
        "prompt",
        "List all my personal private GitHub repositories. Github username vados1. You are authenticated to github",
    )

    github_mcp_client = MCPClient(
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

    with github_mcp_client:
        github_tool_list = github_mcp_client.list_tools_sync()

        naming_agent = Agent(
            system_prompt=NAMING_SYSTEM_PROMPT,
            model="us.anthropic.claude-sonnet-4-20250514-v1:0",  # Use inference profile
            tools=github_tool_list,
        )

        result = naming_agent(user_message)
        return {"result": result}


if __name__ == "__main__":
    app.run()
