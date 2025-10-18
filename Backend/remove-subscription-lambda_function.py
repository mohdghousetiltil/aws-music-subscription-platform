import json
import boto3


"""
Delete item logic adapted from Boto3 documentation:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.delete_item
"""


#Initialize a DynamoDB resource and point to the subscription table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('subscription')

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    try:
        body = json.loads(event.get('body', '{}'))

        email = body.get('email')
        title = body.get('title')

#Return 400 Bad Request if either email or title are missing 
        if not email or not title:
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': json.dumps({'message': 'Email and title are required'})
            }

        #Deleting item with composite key: email (partition) + title (sort)
        response = table.delete_item(
            Key={
                'email': email,
                'title': title
            }
        )

#Return 200 OK with a success message after deletion
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'message': 'Subscription removed'})
        }
#Catch and log any server-side errors, return 500 Internal Server Error
    except Exception as e:
        print("Error removing subscription:", str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'message': 'Server error: ' + str(e)})
        }
