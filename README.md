# Restaurant-Review-ETL-Pipeline


# S3 JSON Uploader

A Python CLI application that randomly selects and uploads JSON files from a specified folder to an AWS S3 bucket at regular intervals.

## Requirements

- Python 3.11
- AWS account with S3 access
- Required Python packages (see requirements.txt)

## AWS Setup Instructions

### 1. Create S3 Bucket

1. Log into AWS Management Console
2. Navigate to S3 service
3. Make sure you're in the correct AWS Region
4. Click "Create bucket"
5. Configure bucket settings:
   - Choose `General purpose` bucket type
   - Choose a globally unique bucket name (this will be your `S3_BUCKET_NAME` in .env)
   - Leave most settings as default
   - Click "Create bucket"

### 2. Create IAM User and Policy

1. Go to IAM service in AWS Console
2. Click "Users" → "Create user"
3. Give your user a name (e.g., "s3-uploader")
4. Do NOT check the box next to "Provide user access to the AWS Management Console"
5. Click "Next: Permissions"
6. Click "Attach policies directly"
7. Create a new policy (Button in Policy section)
8. On the next page, choose JSON in the Policy Editor
9. Copy and paste the following
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Action": ["s3:PutObject", "s3:GetObject", "s3:ListBucket"],
         "Resource": [
           "arn:aws:s3:::YOUR-BUCKET-NAME",
           "arn:aws:s3:::YOUR-BUCKET-NAME/*"
         ]
       }
     ]
   }
   ```
   (Replace `YOUR-BUCKET-NAME` with your actual bucket name)
10. Give the policy a name (e.g., "S3UploadAccess")
11. Attach this policy to your user
12. Complete the user creation
13. **IMPORTANT**: Save the Access Key ID and Secret Access Key - these are your credentials for the .env file

## Project Setup

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your AWS credentials:
   ```bash
   cp .env.example .env
   ```
4. Edit the `.env` file with your AWS credentials:
   ```
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   AWS_REGION=your_aws_region
   S3_BUCKET_NAME=your_bucket_name
   ```
5. Update the configuration variables in `src/s3_uploader.py`:
   - `DATA_FOLDER`: Path to your JSON files
   - `UPLOAD_INTERVAL`: Time between uploads in seconds

## Usage

Run the script:

```bash
python src/s3_uploader.py
```

The script will:

1. Load AWS credentials from the .env file
2. Connect to your S3 bucket
3. Randomly select a JSON file from the specified folder
4. Upload it to the S3 bucket
5. Wait for the specified interval
6. Repeat the process

## Project Structure

```
.
├── data-news-articles/     # Folder containing JSON files to upload
├── src/
│   └── s3_uploader.py     # Main script
├── .env                   # AWS credentials (not in version control)
├── .env.example          # Template for .env file
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your AWS credentials secure
- Use appropriate IAM roles and permissions for S3 access
