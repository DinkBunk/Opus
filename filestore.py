import boto3
import os

# Replace 'your_access_key', 'your_secret_access_key', and 'your_region' with your actual AWS credentials
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY')
aws_secret_access_key = os.environ.get('AWS_SECRET')
aws_region = 'us-east-2'

session = boto3.Session(
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    region_name=aws_region
)

s3 = session.client('s3')