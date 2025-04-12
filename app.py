import streamlit as st
import boto3
import os
from dotenv import load_dotenv
from datetime import datetime
import pandas as pd

# Load AWS keys from .env
load_dotenv()

# AWS credentials & bucket info
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
REGION = "us-east-1"

# S3 client setup
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=REGION
)

# Streamlit UI
st.title("📤 Upload CSV")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Show preview
    df = pd.read_csv(uploaded_file)
    st.write("📄 File Preview:")
    st.dataframe(df.head())

    # Reset file pointer so boto3 can read the file again
    uploaded_file.seek(0)

    # Upload to S3
    if st.button("Upload to S3"):
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        s3_filename = f"uploads/{timestamp}_{uploaded_file.name}"

        try:
            s3.upload_fileobj(uploaded_file, S3_BUCKET, s3_filename)
            st.success(f"✅ Uploaded to S3 as `{s3_filename}`")
        except Exception as e:
            st.error(f"❌ Upload failed: {e}")