import json
import boto3

"""
Code inspired by AWS Lambda + DynamoDB get_item usage:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.get_item
"""


#Initialize DynamoDB resource and pointing LoginPage table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('LoginPage')

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))

#Parse the incoming JSON body to extract email and password
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        password = body.get('password')

# Return 400 Bad Request if email or password are incorrect 
        if not email or not password:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': 'Email and password required'})
            }

#Retrieve user data from DynamoDB using email as the key
        response = table.get_item(Key={'email': email})

        if 'Item' not in response:
            return {
                'statusCode': 401,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': 'User not found'})
            }

#Return 200 OK with a success message after logging in
        user = response['Item']
        if user['password'] == password:
            return {
                'statusCode': 200,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({
                    'message': 'Login successful',
                    'user_name': user.get('user_name', '')
                })
            }
        else:
            return {
                'statusCode': 401,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': 'Invalid password'})
            }

#Catch and log any server-side errors, return 500 Internal Server Error
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': str(e)})
        }
