import json
import os

import boto3
from dotenv import load_dotenv

client = boto3.client('bedrock-agentcore', region_name='us-east-1')
payload = json.dumps({"prompt": "Explain machine learning in simple terms"})

load_dotenv()
aws_account_id = os.environ.get('AWS_ACCOUNT_ID')

response = client.invoke_agent_runtime(
    agentRuntimeArn=f'arn:aws:bedrock-agentcore:us-east-1:{aws_account_id}:runtime/dragon-apjZIHELxr',
    runtimeSessionId='dfmeoagmreaklgmrkleafremoigrmtesogmtrskhmtkrlshmt',  # Must be 33+ chars
    payload=payload,
    qualifier="DEFAULT"  # Optional
)
response_body = response['response'].read()
response_data = json.loads(response_body)
print("Agent Response:", response_data)
