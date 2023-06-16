import boto3
import os

# Replace 'your_access_key', 'your_secret_access_key', and 'your_region' with your actual AWS credentials
aws_access_key_id = os.environ.get('AWS_ACCESS_KEY')
aws_secret_access_key = os.environ.get('AWS_SECRET')
aws_region = 'us-east-2'

bucket = 'opus-training-data'
resource = "s3"


class BlobDelegate:
    def __init__(self):
        self.session = boto3.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=aws_region
        )


    def upload_blob(self, blob_id, file_path):
        with open(file_path, 'rb') as data:
            self.client.upload_fileobj(data, bucket, blob_id)

    def download_blob(self, _id, filename):
        self.session.resource(resource).Bucket(bucket).download_file(
        Key=_id, Filename=f"/tmp/{filename}.wav")
