import boto3

"""
Code adapted from AWS DynamoDB create_table example:
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.01.html
"""


# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

try:
    # Create the 'music' table
    table = dynamodb.create_table(
        TableName='music',
        KeySchema=[
            {'AttributeName': 'title', 'KeyType': 'HASH'},   # Partition key
            {'AttributeName': 'artist', 'KeyType': 'RANGE'}  # Sort key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'title', 'AttributeType': 'S'},
            {'AttributeName': 'artist', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 5,
            'WriteCapacityUnits': 5
        }
    )

    # Wait for the table to become active
    table.meta.client.get_waiter('table_exists').wait(TableName='music')
    print("Table 'music_demo' created successfully.")

except dynamodb.meta.client.exceptions.ResourceInUseException:
    print("Table 'music_demo' already exists.")

except Exception as e:
    print(f"Error creating table: {e}")
