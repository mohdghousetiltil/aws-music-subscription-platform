import boto3
import requests
import json
import os
from urllib.parse import urlparse

"""
S3 image upload logic inspired by AWS Boto3 put_object example:
https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_object
"""

BUCKET_NAME = 's3musicapp'
FOLDER = 'artist-images/'

#Loading song data from 2025a1.json file
with open('2025a1.json', 'r') as f:
    songs = json.load(f)["songs"]

#Loading S3 credentials
s3 = boto3.client('s3', region_name='us-east-1')
uploaded = set()

for song in songs:
    full_url = song.get("img_url")
    if not full_url or full_url in uploaded:
        continue

    filename = os.path.basename(full_url)  #Extracting the file names
    s3_key = FOLDER + filename

    try:
        #Downloading from Github URL given
        response = requests.get(full_url)
        response.raise_for_status()

        #Uploading to S3 using only the filename not by full URL
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=s3_key,
            Body=response.content,
            ContentType='image/jpeg'
        )

        print(f" Uploaded to S3 as: {s3_key}")
        uploaded.add(full_url)

    except Exception as e:
        print(f" Failed to upload {filename}: {e}")
