import boto3

class BlobDelegate:
    def __init__(self, s3_bucket):
        self.s3 = boto3.client('s3')
        self.bucket = s3_bucket

    def upload_blob(self, blob_id, file_path):
        with open(file_path, 'rb') as data:
            self.s3.upload_fileobj(data, self.bucket, blob_id)

    def get_blob(self, blob_id):
        return self.s3.generate_presigned_url('get_object', Params={'Bucket': self.bucket})
