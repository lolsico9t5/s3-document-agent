# 🤖 S3 Document Intelligence Agent

> **One new tool. One massive capability gap closed.**  
> Built with [Strands Agents SDK](https://strandsagents.com) + Amazon Bedrock + Amazon S3  
> Submitted for the [AWS Weekend Challenge — Give Your Agent a New Tool](https://community.aws/challenges)

---

## 🎬 Demo Video

[![Demo Video](https://img.shields.io/badge/Watch%20Demo-YouTube-red?style=for-the-badge&logo=youtube)](https://youtu.be/oboLywwI_wc)

---

## 🧠 The Agent I Started With

A conversational assistant powered by **Amazon Bedrock** (Amazon Nova Lite) via the **Strands Agents SDK**.

It could reason, answer questions, and hold a conversation — but it was **completely blind to the outside world**. No tools. No external data access.

Ask it to analyze a sales CSV, summarize a policy document, or review a security report sitting in your S3 bucket?

```
User: Analyze the sales data in my S3 bucket under reports/q3-sales-2024.csv

Agent: I'm unable to directly access or analyze data stored in an S3 bucket.
       You could copy and paste the CSV contents here instead...
```

**The gap:** Great at reasoning. Useless with real data.

---

## 🔧 The One New Tool I Added

**Amazon S3 Document Reader** — two focused functions decorated with `@tool` from Strands:

| Tool | What it does |
|------|-------------|
| `read_s3_document(bucket, key)` | Fetches and returns the full text of any file in S3 |
| `list_s3_objects(bucket, prefix)` | Lists available files so the agent can discover documents |

### The entire wiring — 4 lines:

```python
from strands import Agent, tool
import boto3

@tool
def read_s3_document(bucket: str, key: str) -> str:
    """Read and return the contents of a document stored in Amazon S3."""
    s3 = boto3.client("s3")
    response = s3.get_object(Bucket=bucket, Key=key)
    return response["Body"].read().decode("utf-8")

agent = Agent(
    model="amazon.nova-lite-v1:0",
    tools=[read_s3_document],   # ← that's the whole wiring
)
```

Strands handles tool schema generation, invocation, and result injection **automatically**.

---

## ✅ Before vs After

### ❌ Before — Agent WITHOUT S3 Tool

```
User:  Analyze the sales data in my S3 bucket under reports/q3-sales-2024.csv

Agent: I'm unable to directly access or analyze data stored in an S3 bucket.
       You could copy and paste the CSV contents here instead...
```

### ✅ After — Agent WITH S3 Tool

```
User:  Analyze the sales data in my S3 bucket under reports/q3-sales-2024.csv

Agent: [calls read_s3_document("strands-agent-demo-bl7ke8", "reports/q3-sales-2024.csv")]

       Top 3 insights from your Q3 sales data:

       1. 🌎 North America had the highest total revenue at $177,500,
          driven by strong Widget Premium sales.

       2. 🏆 Widget Premium was the top product at $108,750 total revenue
          across all regions.

       3. 📈 The North America + Widget Premium combo peaked at $46,500
          in July — focus marketing efforts here for maximum ROI.
```

**Real data. Real insights. Zero copy-pasting.**

---

## 🏗️ Project Structure

```
s3-document-agent/
├── agent_before.py      # The original agent — no tools
├── agent_after.py       # The upgraded agent — S3 tools wired in
├── s3_tool.py           # The new tool (read_s3_document + list_s3_objects)
├── demo.py              # Full before/after demo script
├── setup_demo_data.py   # Creates S3 bucket with sample files
├── requirements.txt     # Python dependencies
└── README.md
```

---

## 🚀 Run It Yourself

### Prerequisites
- Python 3.10+
- AWS account with S3 and Bedrock access
- Amazon Nova Lite enabled in Bedrock (no use-case form needed)

### Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/s3-document-agent.git
cd s3-document-agent

# 2. Create virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure AWS credentials
aws configure
# Enter your Access Key ID, Secret Key, region (us-east-1)

# 5. Create demo data in S3
python setup_demo_data.py
# Note the bucket name it prints, update DEMO_BUCKET in demo.py

# 6. Run the full demo
python demo.py
```

### IAM Permissions Required
```json
{
  "Effect": "Allow",
  "Action": [
    "s3:GetObject",
    "s3:ListBucket",
    "s3:CreateBucket",
    "s3:PutObject",
    "bedrock:InvokeModel",
    "bedrock:InvokeModelWithResponseStream"
  ],
  "Resource": "*"
}
```

---

## ☁️ AWS Services Used

| Service | Role |
|---------|------|
| **Amazon Bedrock** | Powers agent reasoning via Amazon Nova Lite |
| **Amazon S3** | The new tool — document and dataset retrieval |

---

## 💡 Why This Pattern Matters

This isn't a demo trick. The same `@tool` decorator pattern works for any team:

- **Finance** — analyze expense exports the moment they land in S3
- **DevOps** — read deployment configs or log archives on demand  
- **Compliance** — review policy documents without copy-pasting
- **Data teams** — explore CSVs and JSON exports through natural language

Drop `s3_tool.py` into any existing Strands project and your agent immediately gains access to all your S3 data.

---

## 📦 Requirements

```
strands-agents>=0.1.0
boto3>=1.34.0
botocore>=1.34.0
```

---

*Built for the AWS Weekend Challenge — October 2026*  
*Strands Agents SDK + Amazon Bedrock + Amazon S3*
