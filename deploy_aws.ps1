# 1. Create DynamoDB Table
Write-Host "Creating DynamoDB Table..."
aws dynamodb create-table `
    --table-name Edumanesia_Dashboard `
    --attribute-definitions AttributeName=regency_id,AttributeType=S AttributeName=data_type,AttributeType=S `
    --key-schema AttributeName=regency_id,KeyType=HASH AttributeName=data_type,KeyType=RANGE `
    --billing-mode PAY_PER_REQUEST | Out-Null

# 2. Create IAM Role for Lambda
Write-Host "Creating IAM Role..."
$trustPolicy = @"
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
"@
Set-Content -Path trust-policy.json -Value $trustPolicy

$roleInfo = aws iam create-role --role-name EdumanesiaLambdaRole --assume-role-policy-document file://trust-policy.json | ConvertFrom-Json
$roleArn = $roleInfo.Role.Arn

aws iam attach-role-policy --role-name EdumanesiaLambdaRole --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
aws iam attach-role-policy --role-name EdumanesiaLambdaRole --policy-arn arn:aws:iam::aws:policy/AmazonDynamoDBReadOnlyAccess

# Wait for IAM role propagation
Write-Host "Waiting 10 seconds for IAM role to propagate..."
Start-Sleep -Seconds 10

# 3. Create Lambda Function
Write-Host "Creating Lambda Function..."
$lambdaCode = @"
import { DynamoDBClient } from '@aws-sdk/client-dynamodb';
import { DynamoDBDocumentClient, QueryCommand } from '@aws-sdk/lib-dynamodb';

const client = new DynamoDBClient({});
const dynamo = DynamoDBDocumentClient.from(client);
const TABLE_NAME = 'Edumanesia_Dashboard';

export const handler = async (event) => {
    const regencyId = event.queryStringParameters?.regency_id;
    if (!regencyId) {
        return { statusCode: 400, body: JSON.stringify({ error: 'regency_id dibutuhkan!' }) };
    }
    try {
        const command = new QueryCommand({
            TableName: TABLE_NAME,
            KeyConditionExpression: 'regency_id = :id',
            ExpressionAttributeValues: { ':id': regencyId }
        });
        const response = await dynamo.send(command);
        let dashboardData = {};
        response.Items.forEach(item => {
            dashboardData[item.data_type] = item;
        });
        return {
            statusCode: 200,
            headers: { 
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dashboardData)
        };
    } catch (error) {
        return { statusCode: 500, body: JSON.stringify({ error: error.message }) };
    }
};
"@

Set-Content -Path index.mjs -Value $lambdaCode
Compress-Archive -Path index.mjs -DestinationPath function.zip -Force

$lambdaInfo = aws lambda create-function `
    --function-name GetEdumanesiaData `
    --runtime nodejs20.x `
    --role $roleArn `
    --handler index.handler `
    --zip-file fileb://function.zip | ConvertFrom-Json

$lambdaArn = $lambdaInfo.FunctionArn

# 4. Create API Gateway (HTTP API)
Write-Host "Creating API Gateway..."
$apiInfo = aws apigatewayv2 create-api `
    --name EdumanesiaAPI `
    --protocol-type HTTP `
    --cors-configuration AllowOrigins='*',AllowMethods=GET | ConvertFrom-Json

$apiId = $apiInfo.ApiId
$apiEndpoint = $apiInfo.ApiEndpoint

$integrationInfo = aws apigatewayv2 create-integration `
    --api-id $apiId `
    --integration-type AWS_PROXY `
    --integration-uri $lambdaArn `
    --payload-format-version 2.0 | ConvertFrom-Json

$integrationId = $integrationInfo.IntegrationId

aws apigatewayv2 create-route `
    --api-id $apiId `
    --route-key 'GET /dashboard' `
    --target "integrations/$integrationId" | Out-Null

aws apigatewayv2 create-stage `
    --api-id $apiId `
    --stage-name default `
    --auto-deploy | Out-Null

# Allow API Gateway to invoke Lambda
aws lambda add-permission `
    --function-name GetEdumanesiaData `
    --statement-id apigateway-invoke `
    --action lambda:InvokeFunction `
    --principal apigateway.amazonaws.com `
    --source-arn "arn:aws:execute-api:ap-southeast-1:$($roleArn.Split(':')[4]):$apiId/*/*" | Out-Null

# Cleanup temporary files
Remove-Item -Path trust-policy.json, index.mjs, function.zip -Force

Write-Host "================================"
Write-Host "AWS Setup Complete!"
Write-Host "Your API Endpoint is: $apiEndpoint/dashboard"
Write-Host "================================"
