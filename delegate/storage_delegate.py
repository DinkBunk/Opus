import boto3

class StorageDelegate:
    def __init__(self):
        self.s3 = boto3.client('s3')
        self.bucket_name = 'opus-training-data'

    def save_to_s3(self, file, filename):
        self.s3.upload_fileobj(file, self.bucket_name, filename)

    def load_from_s3(self, filename):
        obj = self.s3.get_object(Bucket=self.bucket_name, Key=filename)
        return obj['Body'].read()