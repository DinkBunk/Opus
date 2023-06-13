import boto3
import os

# Replace 'your_access_key', 'your_secret_access_key', and 'your_region' with your actual AWS credentials
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY')
aws_secret_access_key = os.environ.get('AWS_SECRET')
aws_region = 'us-east-2'


class BlobDelegate:
    def __init__(self):
        session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )
        self.client = session.client('s3')
        self.bucket = 'opus-training-data'

    def upload_blob(self, blob_id, file_path):
        with open(file_path, 'rb') as data:
            self.client.upload_fileobj(data, self.bucket, blob_id)

    def get_blob(self, blob_id):
        return self.client.generate_presigned_url('get_object', Params={'Bucket': self.bucket, 'Key': blob_id})
