## strands agentcore

- Run script from local
```python
python ./strands-agentcore/0_local.py 
```

- Deploy to Amazon Bedrock AgentCore
```python
- curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
- unzip awscliv2.zip
- sudo ./aws/install
- aws configure
- source ./strands-agentcore/.env
- agentcore configure -e ./strands-agentcore/1_agent_core.py 
- agentcore launch --auto-update-on-conflict --env GITHUB_TOKEN=$GITHUB_TOKEN --env ATLASSIAN_EMAIL=$ATLASSIAN_EMAIL --env ATLASSIAN_API_TOKEN=$ATLASSIAN_API_TOKEN --env CONFLUENCE_URL=$CONFLUENCE_URL --env JIRA_URL=$JIRA_URL
- agentcore invoke '{\"prompt\": \"List all my personal private GitHub repositories. Github username vados1. You are authenticated to github. Check KAN-1 Jira ticket and provide a summary of its current status and any pending actions required."}'
- agentcore destroy
- manually delete agentcore memory
```