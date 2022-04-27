import os
import sys
import boto3
from dotenv import load_dotenv
import argparse

load_dotenv(verbose=True)

class AWS():
    def __init__(self) -> None:
        self.region_name = 'us-west-2'
        session = boto3.session.Session(aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                        aws_secret_access_key=os.getenv('AWS_ACCESS_KEY_SECRET'),
                        region_name=self.region_name)
        self.s3_resource = session.resource('s3')

    def make_bucket(self, name, acl):
        return self.s3_resource.create_bucket(Bucket=name, ACL=acl, CreateBucketConfiguration={'LocationConstraint':self.region_name})

    def upload_file_to_bucket(self, bucket_name, file_path, s3_bucket):
        file_dir, file_name = os.path.split(file_path)
        bucket = self.s3_resource.Bucket(bucket_name)
        bucket.upload_file(
            Filename=file_name,
            Key=file_path,
            ExtraArgs={'ACL': 'public-read'}
            )
        return 1
    
    def download_file(self, bucket_name, s3_key, dst_path):
        bucket = self.s3_resource.Bucket(bucket_name)
        bucket.download_file(Key=s3_key, Filename=dst_path)
        return 1


if __name__ == "__main__":
    BUCKET_NAME = "bucketname"
    file_path = "filepath"
    dst_path = "dstpath"

    parser = argparse.ArgumentParser()
    parser.add_argument("--upload", help = "upload file to S3 bucket")
    parser.add_argument("--download", help = "download file from S3 bucket")
    parser.add_argument("--dst_path", help = "destination_path for local")
    parser.add_argument("--file_path", help = "file path in the S3 bucket")

    try:
        args = parser.parse_args()
    except argparse.ArgumentError:
        parser.print_help(sys.stderr)
        sys.exit(1)
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    aws = AWS()
    
    if args.upload:
        if args.file_path:
            file_path = args.file_path
        else:
            print("Pleare provide file path")
            sys.exit(1)
        BUCKET_NAME = args.upload
        s3_msg = aws.upload_file_to_bucket(BUCKET_NAME, file_path)
        print(s3_msg)
        sys.exit(1)
    
    if args.download:
        if args.file_path:
            file_path = args.file_path
        else:
            print("Pleare provide file path")
            sys.exit(1)
        if args.dst_path:
            dst_path = args.dst_path
        else:
            print("Pleare provide local destination path")
            sys.exit(1)
        BUCKET_NAME = args.download
        s3_msg = aws.download_file_from_bucket(BUCKET_NAME, file_path, dst_path)
        print(s3_msg)
        sys.exit(1)
