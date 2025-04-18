# 🍽️ Restaurant Reviews ETL Pipeline
~~~
Team PyCharmers:
- Eva Balogun
- Olivia Mintz
- Nusha Bhat
~~~

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

	1.	Clone the repo
	2.	Set up .env with AWS credentials
	3.	Create S3 bucket and RDS instance
	4.	Deploy Lambda function (with layers and role access)
	5.	Run Streamlit app: streamlit run your-path/app.py
 
 

