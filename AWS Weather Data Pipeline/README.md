# 🌤 AWS Weather Data Pipeline

Automated serverless pipeline that fetches real-time weather data
for 4 Indian cities every hour and sends email summary.

## 🏗 Architecture

EventBridge (hourly) → Lambda (Python) → OpenWeatherMap API → S3 → SES Email

## ⚙️ AWS Services Used

| Service | Purpose |
|---|---|
| AWS Lambda | Fetch weather + save to S3 + send email |
| Amazon EventBridge | Trigger Lambda every hour (cron) |
| Amazon S3 | Store hourly JSON files (date-partitioned) |
| AWS SES | Send hourly weather summary email |
| AWS SSM Parameter Store | Store API key securely |
| AWS IAM | Least-privilege role for Lambda |
| Amazon CloudWatch | Logs + error monitoring |

## 📸 Screenshots

### Lambda Function
![Lambda](images/lambda.png)

### EventBridge Schedule
![EventBridge](images/eventbridge.png)

### Python Code
![Code](images/code.png)

### S3 Bucket Structure
![S3](images/s3.png)

### IAM Role
![IAM](images/iam.png)

### OpenWeatherMap API
![OpenWeatherMap](images/openweather.png)

### Email Output
![Email](images/email.png)

## 📁 S3 Data Structure
weather-pipeline-bucket/
└── weather/
└── mumbai/
└── 2026/
└── 06/
└── 05/
├── 00-00.json
├── 01-00.json

## 🌡️ Cities Tracked

- Mumbai
- Delhi
- Bangalore
- Chennai

## 📧 Sample Email Output



## 🛠️ Setup Guide

### 1. Prerequisites
-- AWS account (free tier)
-- OpenWeatherMap free API key → [openweathermap.org](https://openweathermap.org)
-- Python 3.12

### 2. Store API Key in SSM

-- AWS Console → Systems Manager → Parameter Store → Create parameter
-- Name  : /weather-pipeline/api-key
-- Type  : SecureString
-- Value : your_api_key

### 3. Create S3 Bucket

-- Name   : weather-pipeline-vivek
-- Region : us-east-1
-- Access : private (block all public)

### 4. Create IAM Role

-- Name     : weather-lambda-role
Policies : AmazonS3FullAccess
CloudWatchLogsFullAccess
AmazonSSMReadOnlyAccess
AmazonSESFullAccess

### 5. Deploy Lambda

Runtime : Python 3.12
Timeout : 30 seconds
Memory  : 128 MB
Role    : weather-lambda-role

### 6. Set EventBridge Rule

Rule type : Schedule
Rate      : 1 hour
Target    : weather-ingestion Lambda

### 7. Verify Email in SES
SES Console → Verified Identities → Create Identity → Email


## 💰 Cost

100% AWS Free Tier — $0/month

| Service | Usage | Free Limit |
|---|---|---|
| Lambda | 720 calls/month | 1,000,000/month |
| S3 | ~1.5 MB/month | 5 GB |
| EventBridge | 720 events/month | 14M/month |
| SES | 720 emails/month | 62,000/month |
| SSM | 720 reads/month | 10,000/month |

## 🗂️ Project Structure
 weather-pipeline/
 ├── lambda_function.py   # main Lambda code
 ├── README.md
 └── images/
 ├── lambda.png
 ├── eventbridge.png
 ├── code.png
 ├── s3.png
 ├── iam.png
 ├── openweather.png
 └── email.png

## 🔗 Skills Demonstrated

AWS Lambda · EventBridge · S3 · SES · SSM · IAM · CloudWatch
Python · boto3 · REST APIs · Serverless · Event-driven Architecture
Data Ingestion · Cloud Automation · Security Best Practices
