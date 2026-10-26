"""
BEFORE: Basic Strands Agent with Amazon Bedrock
-----------------------------------------------
This agent can only answer questions from its training data.
It has NO ability to read external documents or data sources.
It cannot access files, S3 buckets, or any live data.

Limitation: Ask it about a specific company report, CSV dataset, or
policy document you uploaded — it simply cannot reach it.
"""

from strands import Agent

# The "before" agent — just a plain Bedrock-powered chatbot
agent = Agent(
    model="amazon.nova-lite-v1:0",
    system_prompt="""You are a helpful document analyst assistant.
    You help users understand and extract insights from documents.
    
    LIMITATION: You can only work with information provided directly 
    in the conversation. You cannot access external files or documents.""",
)

def run_before_demo():
    print("=" * 60)
    print("BEFORE: Agent WITHOUT S3 Tool")
    print("=" * 60)
    print()

    # Demo query — agent will fail to get the real data
    query = "Analyze the sales report I uploaded to my S3 bucket at s3://my-reports/q3-sales-2024.csv and give me a summary."
    print(f"User: {query}")
    print()

    response = agent(query)
    print(f"Agent: {response}")
    print()
    print("^ Notice: The agent admits it cannot access S3. It's blind to your data.")
    print()

if __name__ == "__main__":
    run_before_demo()
