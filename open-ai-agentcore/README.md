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
python ./open-ai-agentcore/src/0_local.py 
```
- Deploy to Amazon Bedrock AgentCore
!!!!!!!!
```python
- aws configure
- source .env
- agentcore configure -e ./src/main_agent_core.py
- agentcore launch --auto-update-on-conflict --env OPENAI_API_KEY=$OPENAI_API_KEY
- agentcore invoke '{\"prompt\": \"Hi"}'
- agentcore destroy
- manually delete agentcore memory
```





!!!!!!!!




- AgentCore Invoke Local

```
curl --location 'localhost:8080/invocations' \
--header 'Content-Type: application/json' \
--data '{
    "prompt": "hi"
}'
```




