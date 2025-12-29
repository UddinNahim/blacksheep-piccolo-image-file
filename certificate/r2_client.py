import boto3
import os
from uuid import uuid4

s3 = boto3.client(
    "s3",
    endpoint_url = os.getenv("endpoint"),
    aws_access_key_id = os.getenv("access_id"),
    aws_secret_access_key=os.getenv("secret"),
    region_name = "auto",
)
BUCKET = os.getenv("bucket")

def upload_certificate_image(file_bytes: bytes, content_type: str) -> str:
    key = f"certificates/{uuid4()}"

    s3.put_object(
        Bucket = BUCKET,
        key = key,
        Body = file_bytes,
        contentType = content_type
    )
    return key