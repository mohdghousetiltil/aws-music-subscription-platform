import json
import boto3


"""
Code adapted from AWS Lambda + DynamoDB put_item example:
https://docs.aws.amazon.com/lambda/latest/dg/with-ddb-example.html
"""


#Initialize a DynamoDB resource and point to the LoginPage table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('LoginPage')

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        email = body.get('email')
        password = body.get('password')
        user_name = body.get('user_name')

#Return 400 Bad Request if any of the fields are missing 
        if not email or not password or not user_name:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': 'All fields are required'})
            }

#Checking  if user already exists
        existing = table.get_item(Key={'email': email})
        if 'Item' in existing:
            return {
                'statusCode': 409,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Content-Type': 'application/json'
                },
                'body': json.dumps({'message': 'Email already registered'})
            }

#Adding a  new user
        table.put_item(Item={
            'email': email,
            'password': password,
            'user_name': user_name
        })

#Return 201 OK with a success message after registration 
        return {
            'statusCode': 201,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Content-Type': 'application/json'
            },
            'body': json.dumps({'message': 'Registration successful'})
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
