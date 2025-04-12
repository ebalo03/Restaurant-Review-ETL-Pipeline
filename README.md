# 🍽️ Restaurant Reviews ETL Pipeline

A Python-based ETL system that uploads restaurant review data to S3, triggers preprocessing via AWS Lambda, and displays analytics through a Streamlit web app hosted on EC2.

---

## ✅ Requirements

- Python 3.11
- AWS account with access to:
  - S3 (Object Storage)
  - Lambda (Serverless Processing)
  - RDS (Relational Database – optional)
  - EC2 (to host the web interface)
- Required Python packages (see `requirements.txt`)

---

## ☁️ AWS Setup Instructions

### 1. Create S3 Buckets

1. Log into AWS Management Console
2. Navigate to **S3**
3. Create two buckets:
   - One for **raw uploads**: `restaurant-etl-input`
   - One for **processed files**: `restaurant-etl-input-processed`
4. Choose `General purpose` bucket type
5. Keep default settings (unless versioning/encryption needed)
6. Click **Create bucket**

### 2. Create IAM User and Policy

1. Go to the **IAM** service
2. Click **Users** → **Create user**
3. Name: `restaurant-etl-user`
4. Uncheck "Console access"


