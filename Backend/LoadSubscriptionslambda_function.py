import json
import boto3
from boto3.dynamodb.conditions import Key
import decimal


"""
Code adapted from AWS Lambda + DynamoDB Query with partition key:
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#querying
"""


#Initialize a DynamoDB resource and point to the subscription table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('subscription')

#Handling Decimal serialization
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

#Altering permissions for CORS_Headers
cors_headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
    'Access-Control-Allow-Methods': 'OPTIONS,GET'
}

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

#Return 400 Bad Request raises if email is missing
    try:
        query_params = event.get('queryStringParameters')
        if not query_params or 'email' not in query_params:
            return {
                'statusCode': 400,
                'headers': cors_headers,
                'body': json.dumps({'message': 'Email is required'})
            }

        email = query_params['email']
        print(f"Looking for subscriptions with email: {email}")

        response = table.query(
            KeyConditionExpression=Key('email').eq(email)
        )
        items = response.get('Items', [])
        print(f"Found {len(items)} items")

#Return 200 if the subscriptions are loaded successfully
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps(items, cls=DecimalEncoder)  #Using encoder here
        }

#Exception will be raised if the error is encountered 
    except Exception as e:
        print("Error during query:", str(e))
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'message': str(e)})
        }
