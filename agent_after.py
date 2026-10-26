"""
AFTER: Strands Agent with Amazon S3 Document Reader Tool
---------------------------------------------------------
The same agent, now equipped with one new tool: the ability to
reach into any S3 bucket, fetch a document, and reason over it.

What changed: Two tools added — read_s3_document and list_s3_objects.
What's now possible: The agent can analyze ANY file the user points it at.

Built with:
  - Strands Agents SDK
  - Amazon Bedrock (Claude 3.5 Sonnet)
  - Amazon S3 (new tool)
"""

from strands import Agent
from s3_tool import read_s3_document, list_s3_objects


# The "after" agent — same brain, now with S3 superpowers
agent = Agent(
    model="amazon.nova-lite-v1:0",
    system_prompt="""You are a powerful document intelligence assistant backed by Amazon Bedrock.

You have the ability to READ real documents directly from Amazon S3 buckets.

When a user asks you to analyze, summarize, or answer questions about a document:
1. Use read_s3_document to fetch it by bucket name and key.
2. If the user only mentions a bucket or folder, use list_s3_objects first to discover files.
3. Analyze the content thoroughly and provide actionable insights.
4. Always cite specific data points, numbers, or sections from the document in your response.

You are no longer limited to training data — you can work with the user's REAL, LIVE data.""",
    tools=[read_s3_document, list_s3_objects],
)


def run_after_demo():
    print("=" * 60)
    print("AFTER: Agent WITH S3 Tool")
    print("=" * 60)
    print()

    # ---------------------------------------------------------------
    # Demo 1: Analyze a specific file
    # ---------------------------------------------------------------
    print("--- Demo 1: Analyze a specific S3 document ---")
    query1 = (
        "Please read the file at bucket 'my-demo-bucket', key 'reports/sample-sales.csv' "
        "and give me a summary of the top insights."
    )
    print(f"User: {query1}")
    print()
    response1 = agent(query1)
    print(f"Agent: {response1}")
    print()

    # ---------------------------------------------------------------
    # Demo 2: Discover what's in a bucket
    # ---------------------------------------------------------------
    print("--- Demo 2: List files in a bucket ---")
    query2 = "What files are available in my S3 bucket called 'my-demo-bucket' under the 'reports/' folder?"
    print(f"User: {query2}")
    print()
    response2 = agent(query2)
    print(f"Agent: {response2}")
    print()


if __name__ == "__main__":
    run_after_demo()
