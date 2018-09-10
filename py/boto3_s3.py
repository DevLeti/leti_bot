import boto3

def download(s3, bucket, obj, local_file_path):
    s3.download_file(bucket, obj, local_file_path)

def upload(s3, local_file_path, bucket, obj):
    s3.upload_file(local_file_path, bucket, obj)

def make_public_read(s3, bucket, key):
    s3.put_object_acl(ACL='public-read', Bucket=bucket, Key=key)

if __name__ == "__main__":
    bucket = "YOUR_BUCKET_NAME"
    obj = "FILE_NAME"
    local_file_path = "LOCAL_FILE_PATH"
    s3 = boto3.client('s3')
    download(s3, bucket, obj, local_file_path)
    upload(s3, local_file_path, bucket, "UPLOAD_FILE_NAME")
    make_public_read(s3, bucket, "UPLOAD_FILE_NAME")
