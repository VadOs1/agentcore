## open-ai-agentcore

python ./open-ai-agentcore/src/0_local.py

#### Amazon Bedrock AgentCore Documentation https://docs.aws.amazon.com/bedrock-agentcore/

#### Amazon Bedrock AgentCore Samples https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main

#### Bedrock AgentCore Starter Toolkit https://github.com/aws/bedrock-agentcore-starter-toolkit

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

- CloudWatch -> Application Signals (APM) -> Transaction Search -> Enable Transaction Search

- aws configure
- source .env
- agentcore configure -e ./src/main_agent_core.py
- agentcore launch --auto-update-on-conflict --env OPENAI_API_KEY=$OPENAI_API_KEY
- agentcore invoke '{\"prompt\": \"Hi"}'
- agentcore destroy
- manually delete agentcore memory


### Create ECR Image for AWS Agent Core (main_strands.py)
- export AWS_REGION=us-east-1 ECR_REPO=agentcore
- export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
- aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com &&
- docker build -t $ECR_REPO .
- docker tag agentcore:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/agentcore:latest
- docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/agentcore:latest