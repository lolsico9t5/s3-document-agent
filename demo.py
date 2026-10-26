"""
Live Demo Script — Run this for your video recording
------------------------------------------------------
This is the single script to run during your demo.
It shows the BEFORE state and the AFTER state side by side.

Before running:
    1. pip install -r requirements.txt
    2. aws configure (set your credentials)
    3. python setup_demo_data.py  (note the bucket name it prints)
    4. Update DEMO_BUCKET below with your actual bucket name
    5. python demo.py
"""

from strands import Agent
from s3_tool import read_s3_document, list_s3_objects


# ── UPDATE THIS after running setup_demo_data.py ──────────────────
DEMO_BUCKET = "strands-agent-demo-bl7ke8"
# ─────────────────────────────────────────────────────────────────


def separator(title: str):
    width = 60
    print()
    print("=" * width)
    print(f"  {title}")
    print("=" * width)
    print()


def show_before():
    separator("BEFORE — Agent WITHOUT S3 Tool")

    # No tools — agent cannot reach any external data
    before_agent = Agent(
        model="amazon.nova-lite-v1:0",
        system_prompt="You are a helpful document assistant. You can only work with information provided directly in the conversation.",
    )

    question = f"Analyze the sales data in my S3 bucket '{DEMO_BUCKET}' under reports/q3-sales-2024.csv"
    print(f"User: {question}")
    print()
    print("Agent:", end=" ", flush=True)

    response = before_agent(question)
    print(response)
    print()
    print("^ The agent can only apologize. It has no way to reach S3.")


def show_after():
    separator("AFTER — Agent WITH Amazon S3 Tool")

    # Equipped with two S3 tools
    after_agent = Agent(
        model="amazon.nova-lite-v1:0",
        system_prompt="""You are a document intelligence assistant powered by Amazon Bedrock.
        
You can READ real files from Amazon S3 using your tools. When asked about a document:
1. Use read_s3_document to fetch it, then analyze it fully.
2. Use list_s3_objects when the user wants to know what files exist.
Always cite specific data from the document in your response.""",
        tools=[read_s3_document, list_s3_objects],
    )

    # Demo 1 — list files
    print("--- Step 1: Discover available documents ---")
    q1 = f"What files are available in my bucket '{DEMO_BUCKET}'?"
    print(f"User: {q1}")
    print()
    print("Agent:", end=" ", flush=True)
    r1 = after_agent(q1)
    print(r1)
    print()

    # Demo 2 — analyze sales CSV
    print("--- Step 2: Analyze the sales report ---")
    q2 = f"Now read reports/q3-sales-2024.csv from bucket '{DEMO_BUCKET}'. What are the top 3 insights from this data? Which region and product are performing best?"
    print(f"User: {q2}")
    print()
    print("Agent:", end=" ", flush=True)
    r2 = after_agent(q2)
    print(r2)
    print()

    # Demo 3 — analyze the security report
    print("--- Step 3: Analyze the security findings ---")
    q3 = f"Read security/assessment-report.json from bucket '{DEMO_BUCKET}'. What are the critical risks and what should we fix first?"
    print(f"User: {q3}")
    print()
    print("Agent:", end=" ", flush=True)
    r3 = after_agent(q3)
    print(r3)
    print()


if __name__ == "__main__":
    show_before()
    show_after()
    separator("Demo Complete")
    print("The agent went from blind to fully document-aware,")
    print("powered by one focused tool: Amazon S3 + Strands Agents SDK.")
    print()
