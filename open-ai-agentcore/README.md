## open-ai-agentcore

- List vector stores

```
curl https://api.openai.com/v1/vector_stores \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -H "OpenAI-Beta: assistants=v2"
```

- Delete vector store

```
curl https://api.openai.com/v1/vector_stores/{id} \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -H "OpenAI-Beta: assistants=v2" \
  -X DELETE
```

- Run script from local
```python
python ./open-ai-agentcore/0_local.py 
```
- Deploy to Amazon Bedrock AgentCore
```python
- curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
- unzip awscliv2.zip
- sudo ./aws/install
- aws configure
- source ./open-ai-agentcore/.env
- agentcore configure -e ./open-ai-agentcore/1_agent_core.py 
- agentcore launch --auto-update-on-conflict --env OPENAI_API_KEY=$OPENAI_API_KEY --env OPENAI_VECTOR_STORE_ID=$OPENAI_VECTOR_STORE_ID
- agentcore invoke '{\"prompt\": \"Hi"}'
- agentcore destroy
- manually delete agentcore memory
```

- Invoke Amazon Bedrock AgentCore from python script
```python
python ./open-ai-agentcore/2_invoke.py
```




