import boto3
import os
import subprocess

def get_account_id():
    sts_client = boto3.client('sts')
    return sts_client.get_caller_identity().get('Account')

def create_s3_bucket(bucket_name, region):
    s3_client = boto3.client('s3', region_name=region)
    try:
        s3_client.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={'LocationConstraint': region}
        )
        print(f"Bucket {bucket_name} created.")
    except s3_client.exceptions.BucketAlreadyOwnedByYou:
        print(f"Bucket {bucket_name} already exists and is owned by you.")
    except Exception as e:
        print(f"Error creating bucket: {e}")

def sync_assets_to_s3(bucket_name):
    try:
        subprocess.run(
            ['aws', 's3', 'sync', '--delete', '--exclude', '*', '--include', 'assets/*', '.', f's3://{bucket_name}'],
            check=True
        )
        print(f"Assets deployed to S3 bucket '{bucket_name}'")
    except subprocess.CalledProcessError as e:
        print(f"Error syncing assets: {e}")

def main():
    aws_region = os.getenv('AWS_REGION', 'us-east-1')
    account_id = get_account_id()
    artifact_bucket = f"sscs-ood-assets-{account_id}"

    create_s3_bucket(artifact_bucket, aws_region)
    sync_assets_to_s3(artifact_bucket)

if __name__ == "__main__":
    main() 