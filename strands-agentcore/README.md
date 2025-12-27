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
- agentcore launch --auto-update-on-conflict --env GITHUB_TOKEN=$GITHUB_TOKEN
- agentcore invoke '{\"prompt\": \"List all my personal private GitHub repositories. Github username vados1. You are authenticated to github"}'
- agentcore destroy
- manually delete agentcore memory
```