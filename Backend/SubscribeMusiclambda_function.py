import json
import boto3

"""
Lambda structure adapted from AWS documentation for writing to DynamoDB:
https://docs.aws.amazon.com/lambda/latest/dg/with-ddb.html
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
        artist = body.get('artist')
        album = body.get('album')
        year = body.get('year')
        artist_image_url = body.get('artist_image_url')

#Return 400 Bad Request if either email,title and artist are missing
        if not (email and title and artist):
            return {
                'statusCode': 400,
                'headers': {
                    'Access-Control-Allow-Origin': '*',
                    'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                    'Access-Control-Allow-Methods': 'OPTIONS,POST'
                },
                'body': json.dumps({'message': 'Missing required fields'})
            }

        table.put_item(Item={
            'email': email,
            'title': title,
            'artist': artist,
            'album': album,
            'year': year,
            'artist_image_url': artist_image_url
        })

#Return 201 once subscription is added
        return {
            'statusCode': 201,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'message': 'Subscription added'})
        }
#Catch and log any server-side errors, return 500 Internal Server Error
    except Exception as e:
        print("ERROR:", str(e))
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token',
                'Access-Control-Allow-Methods': 'OPTIONS,POST'
            },
            'body': json.dumps({'message': str(e)})
        }
