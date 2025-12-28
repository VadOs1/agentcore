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
        "List all my personal private GitHub repositories. Github username vados1. You are authenticated to github. Check KAN-1 Jira ticket and provide a summary of its current status and any pending actions required.",
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

    atlassian_mcp_client = MCPClient(
        lambda: stdio_client(
            StdioServerParameters(
                command="docker",
                args=[
                    "run",
                    "--rm",
                    "-i",
                    "-e",
                    f"JIRA_USERNAME={os.environ.get('ATLASSIAN_EMAIL')}",
                    "-e",
                    f"JIRA_API_TOKEN={os.environ.get('ATLASSIAN_API_TOKEN')}",
                    "-e",
                    f"JIRA_URL={os.environ.get('JIRA_URL')}",
                    "-e",
                    f"CONFLUENCE_USERNAME={os.environ.get('ATLASSIAN_EMAIL')}",
                    "-e",
                    f"CONFLUENCE_API_TOKEN={os.environ.get('ATLASSIAN_API_TOKEN')}",
                    "-e",
                    f"CONFLUENCE_URL={os.environ.get('CONFLUENCE_URL')}",
                    "ghcr.io/sooperset/mcp-atlassian:latest",
                ],
            )
        ),
        startup_timeout=30,
    )

    with github_mcp_client, atlassian_mcp_client:
        github_tool_list = github_mcp_client.list_tools_sync()
        print("Available GitHub tools:", github_tool_list)

        atlassian_tool_list = atlassian_mcp_client.list_tools_sync()
        print("Available Atlassian tools:", atlassian_tool_list)

        tools = github_tool_list + atlassian_tool_list

        naming_agent = Agent(
            system_prompt=NAMING_SYSTEM_PROMPT,
            model="us.anthropic.claude-sonnet-4-20250514-v1:0",  # Use inference profile
            tools=tools,
        )

        result = naming_agent(user_message)
        return {"result": result}


if __name__ == "__main__":
    app.run()
