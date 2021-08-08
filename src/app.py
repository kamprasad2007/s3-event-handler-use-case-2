import boto3
import os
import urllib
import json

def lambda_handler(event, context):
    BUCKET_NAME = urllib.parse.unquote_plus(event['Records'][0]['s3']['bucket']['name'])
    FILE_NAME = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    QUEUE_URL = os.environ.get('QUEUE_URL')

    client = boto3.client('s3')
    result = client.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME) 
    data = result["Body"].read()
    
    queue = boto3.client('sqs')
    queue.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=(json.dumps({"data": data})),
        MessageGroupId='S3FileProcessginGroup',
    )