# lambda handler

import boto3
import pymysql
import pandas as pd
import os
import io
import numpy as np

# Load environment variables
DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_PASSWORD = os.environ['DB_PASSWORD']
DB_NAME = os.environ['DB_NAME']
PROCESSED_BUCKET = 'restaurant-reviews-processed-data'

def lambda_handler(event, context):
    print("✅ Imported numpy version:", np.__version__)
    print("✅ Imported pandas version:", pd.__version__)
    print("Lambda triggered by event:", event)

    # get file from S3
    s3 = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    print(f"Fetching file: s3://{bucket}/{key}")
    response = s3.get_object(Bucket=bucket, Key=key)
    df = pd.read_csv(io.BytesIO(response['Body'].read()))

    # /debugging
    print("Raw DataFrame preview:\n", df.head().to_string())
    print("NaN count per column:\n", df.isna().sum())

    # drop last 3 columns
    df_clean = df.iloc[:, :-3]

    if df_clean.empty:
        print("DataFrame is empty after cleaning.")
        return {
            'status': 'error',
            'message': 'No valid data in CSV after cleaning.'
        }

    print("Available columns:", df_clean.columns.tolist())
    print("Cleaned DataFrame preview:\n", df_clean.head().to_string())

    # extract summary values
    restaurant_name = df_clean['Restaurant'].iloc[0]
    avg_rating = df_clean['Rating'].astype(float).mean()
    total_reviews = len(df_clean)

    # save cleaned file to another bucket
    output_csv = df_clean.to_csv(index=False)
    s3.put_object(Bucket=PROCESSED_BUCKET, Key=key, Body=output_csv)
    print(f"Uploaded cleaned file to {PROCESSED_BUCKET}/{key}")

    # insert summary into RDS
    connection = pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    with connection.cursor() as cursor:
        cursor.execute("""
            INSERT INTO reviews_summary (restaurant_name, avg_rating, total_reviews)
            VALUES (%s, %s, %s)
        """, (restaurant_name, avg_rating, total_reviews))
        connection.commit()
        print("Inserted summary row into RDS.")

    return {
        'status': 'success',
        'file': key,
        'restaurant': restaurant_name,
        'avg_rating': avg_rating,
        'total_reviews': total_reviews
    }
