import boto3
import csv
import logging
import os
import tempfile

s3 = boto3.client('s3')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    
    # pull the bucket name from the event
    bucket = event['Records'][0]['s3']['bucket']['name']

    # get the key for the file uploaded
    key = event['Records'][0]['s3']['object']['key']

    logger.info(f"Triggered by upload of file: {key} in bucket: {bucket}")

    # Download the CSV to Lambda's temporary storage
    with tempfile.NamedTemporaryFile(suffix='.csv') as temp_csv:
        s3.download_file(bucket, key, temp_csv.name)

    # RDS connection setup
        conn = psycopg2.connect(
        host='ds4300-project-rds-db.cad8e6aqaozu.us-east-1.rds.amazonaws.com',
        database='ds4300-project-rds-db',
        user='admin',
        password='ds4300finalproject',
        port=3306
    )
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute(
            "INSERT INTO preprocessed_table (col1, col2) VALUES (%s, %s)",
            (row['processed_col'], row['other_col'])
        )

    conn.commit()
    cursor.close()
    conn.close()


        # Open the file and analyze CSV content
        with open(temp_csv.name, newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            rows = list(reader)
            row_count = len(rows)
            col_count = len(rows[0]) if row_count > 0 else 0

            logger.info(f"CSV file {key} has {row_count} rows and {col_count} columns.")

        # Move (copy then delete) the file to the processed bucket
        dest_bucket = 'ds4300-resturant-output'
        copy_source = {'Bucket': bucket, 'Key': key}

        s3.copy_object(Bucket=dest_bucket, Key=key, CopySource=copy_source)
        s3.delete_object(Bucket=bucket, Key=key)

        logger.info(f"Moved file {key} from bucket {bucket} to bucket {dest_bucket}.")



    return {
        'statusCode': 200,
        'body': f"Processed and moved {key} successfully."
    }

    return {
        'statusCode': 200,
        'body': f"Processed and moved {key} successfully."
    }
