#!/bin/bash
echo "Initializing LocalStack AWS S3 Buckets..."
awslocal s3 mb s3://zomato-data-lake
awslocal s3 ls
echo "LocalStack S3 Bucket zomato-data-lake created successfully!"
