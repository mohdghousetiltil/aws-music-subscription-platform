import boto3
import json

"""
JSON loading and DynamoDB insertion adapted from AWS and Python JSON examples:
https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
"""

# Connect to DynamoDB
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('music')

# Load data from JSON file
with open("2025a1.json", "r") as f:
    data = json.load(f)
    songs = data["songs"]  #Extract the list of songs

# Insert each song into DynamoDB
for song in songs:
    try:
        # Rename img_url to match your table attribute if needed (e.g., image_url)
        song["image_url"] = song.pop("img_url")
        table.put_item(Item=song)
        print(f"Inserted: {song['title']} by {song['artist']}")
    except Exception as e:
        print(f"Failed to insert {song['title']}: {e}")
