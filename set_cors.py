"""
Run once to apply CORS rules to the DO Spaces bucket.
Usage: python set_cors.py
"""

import os
from pathlib import Path

import boto3
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

client = boto3.client(
    "s3",
    region_name=os.getenv("SPACE_REGION"),
    endpoint_url=os.getenv("SPACE_URL"),
    aws_access_key_id=os.getenv("SPACE_ID"),
    aws_secret_access_key=os.getenv("SPACE_SECRET"),
)

bucket = os.getenv("SPACE_BUCKET")

cors_config = {
    "CORSRules": [
        {
            "AllowedHeaders": ["*"],
            "AllowedMethods": ["GET", "HEAD"],
            "AllowedOrigins": [
                "http://localhost:5173",
                "http://localhost:5174",
                "http://localhost:3000",
                # Add your production domain below, e.g.:
                # "https://yourdomain.com",
            ],
            "ExposeHeaders": ["Content-Length", "Content-Type"],
            "MaxAgeSeconds": 3600,
        }
    ]
}

client.put_bucket_cors(Bucket=bucket, CORSConfiguration=cors_config)
print(f"✓ CORS rules applied to bucket: {bucket}")

# Verify
result = client.get_bucket_cors(Bucket=bucket)
for rule in result["CORSRules"]:
    print(f"  Origins : {rule['AllowedOrigins']}")
    print(f"  Methods : {rule['AllowedMethods']}")
