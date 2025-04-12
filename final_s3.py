
# user uploads csv file to s3 input bucket
# MAKE SURE .ENV IS UPDATED FIRST

import os
import boto3
from dotenv import load_dotenv

# credentials from .env
load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

# file to upload
FILE_PATH = "restaurant_reviews.csv"
S3_UPLOAD_KEY = f"uploads/{os.path.basename(FILE_PATH)}"  # S3 key inside the bucket

def upload_to_s3():
    s3 = boto3.client("s3",
                      region_name=AWS_REGION,
                      aws_access_key_id=AWS_ACCESS_KEY_ID,
                      aws_secret_access_key=AWS_SECRET_ACCESS_KEY)

    try:
        with open(FILE_PATH, "rb") as file:
            s3.upload_fileobj(file, S3_BUCKET_NAME, S3_UPLOAD_KEY)
        print(f"✅ Successfully uploaded {FILE_PATH} to {S3_BUCKET_NAME}/{S3_UPLOAD_KEY}")
    except Exception as e:
        print(f"❌ Upload failed: {str(e)}")

if __name__ == "__main__":
    upload_to_s3()
