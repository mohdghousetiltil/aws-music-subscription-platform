import json
import boto3
import decimal
from boto3.dynamodb.conditions import Attr

"""
Code structure based on AWS DynamoDB Scan with FilterExpression:
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html#filtering-results
"""


#Setup DynamoDB resource and table
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('music')

#Base S3 URL for artist images
S3_BASE_URL = "https://s3musicapp.s3.us-east-1.amazonaws.com/artist-images/"

#Convert Decimal to int/float for JSON
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return float(obj) if '.' in str(obj) else int(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    print("Received event:", json.dumps(event))

    try:
        body = json.loads(event.get('body', '{}'))

        title = body.get('title')
        artist = body.get('artist')
        album = body.get('album')
        year = body.get('year')
# Return 400 Bad Request if either title or artist or album or year are missing
        if not (title or artist or album or year):
            return {
                'statusCode': 400,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'message': 'At least one field is required'})
            }

#Build scan filter expression
        filter_expr = None

        if title:
            filter_expr = Attr("title").contains(title) if not filter_expr else filter_expr & Attr("title").contains(title)
        if artist:
            filter_expr = Attr("artist").contains(artist) if not filter_expr else filter_expr & Attr("artist").contains(artist)
        if album:
            filter_expr = Attr("album").contains(album) if not filter_expr else filter_expr & Attr("album").contains(album)
        if year:
            filter_expr = Attr("year").eq(int(year)) if not filter_expr else filter_expr & Attr("year").eq(int(year))

        result = table.scan(FilterExpression=filter_expr)
        items = result.get('Items', [])

        if not items:
            return {
                'statusCode': 404,
                'headers': {'Access-Control-Allow-Origin': '*'},
                'body': json.dumps({'message': 'No result is retrieved. Please query again.'})
            }

#Ensure image_url has full path
        for item in items:
            if 'image_url' in item and not item['image_url'].startswith("http"):
                item['image_url'] = f"{S3_BASE_URL}{item['image_url']}"
            elif 'image_url' not in item or not item['image_url']:
                artist_name = item.get('artist', '').strip().replace(' ', '_')
                item['image_url'] = f"{S3_BASE_URL}{artist_name}.jpg"

#Return 200 after querying the music details
        return {
            'statusCode': 200,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps(items, cls=DecimalEncoder)
        }
#Catch and log any server-side errors, return 500 Internal Server Error
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {'Access-Control-Allow-Origin': '*'},
            'body': json.dumps({'message': str(e)})
        }
