## agentcore

#### Amazon Bedrock AgentCore Documentation https://docs.aws.amazon.com/bedrock-agentcore/
#### Amazon Bedrock AgentCore Samples https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main
#### OpenAI Vector Store API reference  https://platform.openai.com/docs/api-reference/vector-stores/list

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

- AgentCore Invoke Local

```
curl --location 'localhost:8080/invocations' \
--header 'Content-Type: application/json' \
--data '{
    "prompt": "hi"
}'
```
