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
