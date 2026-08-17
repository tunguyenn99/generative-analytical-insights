import os
import glob
import boto3
from botocore.exceptions import EndpointConnectionError, ClientError

LOCALSTACK_ENDPOINT = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
BUCKET_NAME = "zomato-data-lake"

def upload_raw_data_to_s3(data_dir="data/raw"):
    s3_client = boto3.client(
        "s3",
        endpoint_url=LOCALSTACK_ENDPOINT,
        aws_access_key_id="test",
        aws_secret_access_key="test",
        region_name="us-east-1"
    )

    try:
        # Check or create bucket
        existing_buckets = [b["Name"] for b in s3_client.list_buckets().get("Buckets", [])]
        if BUCKET_NAME not in existing_buckets:
            s3_client.create_bucket(Bucket=BUCKET_NAME)
            print(f"📦 Created LocalStack S3 Bucket: 's3://{BUCKET_NAME}'")
        else:
            print(f"📦 LocalStack S3 Bucket 's3://{BUCKET_NAME}' already exists.")

        csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
        for filepath in csv_files:
            filename = os.path.basename(filepath)
            table_name = os.path.splitext(filename)[0]
            s3_key = f"raw/{table_name}/{filename}"
            s3_client.upload_file(filepath, BUCKET_NAME, s3_key)
            print(f"  └─ Uploaded {filename} ➔ s3://{BUCKET_NAME}/{s3_key}")

        print("\n✅ All raw datasets successfully landed in AWS LocalStack S3!")
        return True

    except (EndpointConnectionError, ClientError, Exception) as e:
        print(f"⚠️ Notice: LocalStack S3 endpoint at {LOCALSTACK_ENDPOINT} is currently offline.")
        print(f"   Using Direct Local File Landing Zone ('{data_dir}') for DuckDB & dbt pipelines.")
        return False

if __name__ == "__main__":
    upload_raw_data_to_s3()
