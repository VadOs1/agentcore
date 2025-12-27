import boto3
import json

client = boto3.client("bedrock-agentcore", region_name="us-east-1")
payload = json.dumps({"prompt": "Explain machine learning in simple terms"})

response = client.invoke_agent_runtime(
    agentRuntimeArn="arn:aws:bedrock-agentcore:us-east-1:065320792144:runtime/dragon-q9lwny7L3G",
    runtimeSessionId="efwefewfewfewfewfewegrthtrhrththrthtrhtrhrthrthrthtrhrthrthrthrthrwthrthrthrthrthrthrth",  # Must be 33+ char. Every new SessionId will create a new MicroVM
    payload=payload,
)
response_body = response["response"].read()
response_data = json.loads(response_body)
print("Agent Response:", response_data)
