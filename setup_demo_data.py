"""
Demo Setup Script
-----------------
Run this ONCE before recording your demo video.
It creates a real S3 bucket and uploads sample documents
so the agent has real data to analyze.

Usage:
    python setup_demo_data.py

Requirements:
    - AWS credentials configured (aws configure)
    - IAM permissions: s3:CreateBucket, s3:PutObject, s3:GetObject, s3:ListBucket
"""

import boto3
import json
import random
import string
from botocore.exceptions import ClientError


# ── Sample data files ────────────────────────────────────────────

SAMPLE_SALES_CSV = """date,region,product,units_sold,revenue,cost
2024-01-15,North America,Widget Pro,450,22500.00,13500.00
2024-01-15,Europe,Widget Pro,320,16000.00,9600.00
2024-01-15,Asia Pacific,Widget Basic,780,19500.00,7800.00
2024-02-15,North America,Widget Pro,510,25500.00,15300.00
2024-02-15,Europe,Widget Basic,410,10250.00,4100.00
2024-02-15,Asia Pacific,Widget Pro,290,14500.00,8700.00
2024-03-15,North America,Widget Premium,220,33000.00,15400.00
2024-03-15,Europe,Widget Pro,380,19000.00,11400.00
2024-03-15,Asia Pacific,Widget Basic,920,23000.00,9200.00
2024-07-15,North America,Widget Premium,310,46500.00,21700.00
2024-07-15,Europe,Widget Premium,195,29250.00,13650.00
2024-07-15,Asia Pacific,Widget Pro,540,27000.00,16200.00
2024-08-15,North America,Widget Pro,480,24000.00,14400.00
2024-08-15,Europe,Widget Basic,640,16000.00,6400.00
2024-08-15,Asia Pacific,Widget Premium,260,39000.00,18200.00
2024-09-15,North America,Widget Basic,820,20500.00,8200.00
2024-09-15,Europe,Widget Premium,175,26250.00,12250.00
2024-09-15,Asia Pacific,Widget Pro,490,24500.00,14700.00
"""

SAMPLE_POLICY_MD = """# Remote Work Policy

**Version:** 3.2  
**Effective Date:** January 1, 2024  
**Owner:** People Operations

## 1. Eligibility

All full-time employees who have completed their 90-day onboarding period are 
eligible for remote work arrangements. Contractors and part-time staff may 
request remote work on a case-by-case basis with manager approval.

## 2. Work Hours and Availability

- **Core hours:** 10:00 AM – 3:00 PM in the employee's primary time zone
- Employees must respond to messages within **2 hours** during core hours
- Calendar must reflect availability and be kept up to date
- Video should be enabled for all team meetings unless circumstances prevent it

## 3. Equipment and Security

The company provides:
- MacBook Pro (14" or 16" depending on role)
- External monitor (27" 4K)
- Noise-canceling headset

Employees are responsible for:
- A reliable internet connection (minimum **50 Mbps** download)
- A dedicated, distraction-free workspace
- Completing annual security awareness training

All company data must be handled per the Information Security Policy.
VPN must be active when accessing internal systems.

## 4. Performance and Accountability

Remote employees are evaluated on outcomes, not hours logged. 
Managers conduct monthly 1:1 check-ins and quarterly performance reviews.

Failure to meet availability, communication, or performance standards 
may result in revocation of remote work privileges.

## 5. Expenses

| Category               | Monthly Allowance |
|------------------------|-------------------|
| Internet               | $60               |
| Office supplies        | $30               |
| Co-working space       | $200 (if needed)  |

Receipts required for all reimbursements over $25.

## 6. Exceptions

Exceptions to this policy require VP-level approval and must be documented 
in the HR system within 5 business days.
"""

SAMPLE_FINDINGS_JSON = """{
  "report_type": "Security Assessment",
  "assessment_date": "2024-09-30",
  "scope": "Production AWS Environment",
  "risk_summary": {
    "critical": 2,
    "high": 7,
    "medium": 14,
    "low": 23,
    "informational": 11
  },
  "critical_findings": [
    {
      "id": "CRIT-001",
      "title": "S3 Bucket with Public Access Enabled",
      "affected_resource": "arn:aws:s3:::legacy-app-uploads",
      "description": "The bucket has Block Public Access disabled and a bucket policy granting s3:GetObject to '*'. Any object uploaded becomes publicly readable.",
      "recommendation": "Enable S3 Block Public Access on the bucket and account level. Audit existing objects for sensitive data.",
      "cvss_score": 9.1,
      "status": "Open"
    },
    {
      "id": "CRIT-002",
      "title": "Root Account Used for Daily Operations",
      "affected_resource": "AWS Account Root",
      "description": "CloudTrail logs show the root account logged in 14 times in the past 30 days for routine API operations. Root should only be used for tasks requiring it.",
      "recommendation": "Create IAM users/roles with least-privilege access. Enable MFA on root. Remove root access keys if present.",
      "cvss_score": 9.8,
      "status": "Open"
    }
  ],
  "top_recommendation": "Address both critical findings within 72 hours. Schedule a hardening sprint for all high-severity findings within the next two-week cycle."
}
"""


def create_bucket_and_upload():
    s3 = boto3.client("s3")
    
    # Use a fixed bucket name or generate a unique one
    suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    bucket_name = f"strands-agent-demo-{suffix}"

    region = boto3.session.Session().region_name or "us-east-1"

    print(f"Creating bucket: {bucket_name} in {region}")
    
    try:
        if region == "us-east-1":
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
        print(f"  ✓ Bucket created")
    except ClientError as e:
        print(f"  ✗ Failed to create bucket: {e}")
        return None

    # Upload sample files
    files = [
        ("reports/q3-sales-2024.csv", SAMPLE_SALES_CSV, "text/csv"),
        ("policies/remote-work-policy.md", SAMPLE_POLICY_MD, "text/markdown"),
        ("security/assessment-report.json", SAMPLE_FINDINGS_JSON, "application/json"),
    ]

    for key, content, content_type in files:
        try:
            s3.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=content.encode("utf-8"),
                ContentType=content_type,
            )
            print(f"  ✓ Uploaded: s3://{bucket_name}/{key}")
        except ClientError as e:
            print(f"  ✗ Failed to upload {key}: {e}")

    print()
    print("=" * 60)
    print("SETUP COMPLETE — use these in your demo:")
    print("=" * 60)
    print(f"  Bucket name : {bucket_name}")
    print(f"  Sales CSV   : reports/q3-sales-2024.csv")
    print(f"  Policy doc  : policies/remote-work-policy.md")
    print(f"  Security    : security/assessment-report.json")
    print()
    print(f"Update DEMO_BUCKET in demo.py with: '{bucket_name}'")
    print()
    return bucket_name


if __name__ == "__main__":
    create_bucket_and_upload()
