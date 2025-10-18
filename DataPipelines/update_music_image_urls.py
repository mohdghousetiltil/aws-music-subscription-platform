import boto3
import json
import os

"""
DynamoDB update_item logic based on AWS example:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.update_item
"""

#Configuring table name andx URL details
TABLE_NAME = 'music'
BUCKET_BASE_URL = 'https://s3musicapp.s3.us-east-1.amazonaws.com/artist-images/'

#Connecting to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table(TABLE_NAME)

#Load songs from JSON file
with open('2025a1.json', 'r') as f:
    songs = json.load(f)["songs"]

#Updating each record
for song in songs:
    title = song["title"]
    artist = song["artist"]
    img_filename = os.path.basename(song["img_url"])  #Getting only filename
    s3_url = BUCKET_BASE_URL + img_filename

    try:
        table.update_item(
            Key={
                "title": title,
                "artist": artist
            },
            UpdateExpression="SET image_url = :url",
            ExpressionAttributeValues={
                ":url": s3_url
            }
        )
        print(f"Updated: {title} by {artist} → {img_filename}")
    except Exception as e:
        print(f"Failed to update {title} by {artist}: {e}")
