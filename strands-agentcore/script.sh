# Register the task definition
aws ecs register-task-definition --cli-input-json file://task-definition.json

# Create or update the service
aws ecs create-service \
  --cluster your-cluster-name \
  --service-name mcp-atlassian-service \
  --task-definition mcp-atlassian-server \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-xxxxx],securityGroups=[sg-xxxxx],assignPublicIp=ENABLED}"