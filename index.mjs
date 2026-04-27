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
