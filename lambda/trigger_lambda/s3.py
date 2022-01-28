import boto3

s3client = boto3.client("s3")


def download_file(bucket, key, path_prefix, filename):
    with open(path_prefix + filename, "wb") as data:
        s3client.download_fileobj(bucket, key, data)
    return True


def upload_file(path, filename, bucket, key):
    with open(path + filename, "rb") as data:
        s3client.upload_fileobj(data, bucket, key)
    return True


def delete_file(bucket, key):
    s3client.delete_object(Bucket=bucket, Key=key)
    return True
