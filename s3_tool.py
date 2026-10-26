"""
The New Tool: Amazon S3 Document Reader
----------------------------------------
This module defines the S3 tool that gives the agent the ability to:
  1. Read any text file, CSV, JSON, or Markdown from an S3 bucket
  2. List objects in a bucket/prefix so the agent can discover available files
  3. Return the content to the agent for analysis

This is the single capability that transforms the agent from a
closed chatbot into a dynamic document intelligence system.
"""

import boto3
import json
from botocore.exceptions import ClientError, NoCredentialsError
from strands import tool


@tool
def read_s3_document(bucket: str, key: str) -> str:
    """
    Read and return the contents of a document stored in Amazon S3.

    Use this tool whenever the user wants to analyze, summarize, or ask
    questions about a file stored in S3. Supports text files, CSVs,
    JSON files, Markdown documents, and other text-based formats.

    Args:
        bucket: The S3 bucket name (e.g., 'my-company-reports')
        key: The S3 object key / file path (e.g., 'reports/q3-sales.csv')

    Returns:
        The full text content of the file, or an error message if the
        file cannot be read.
    """
    s3 = boto3.client("s3")

    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        content = response["Body"].read()

        # Decode bytes to string — handle common encodings gracefully
        try:
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            text = content.decode("latin-1")

        # Cap at ~50KB to avoid overwhelming the context window
        MAX_CHARS = 50_000
        if len(text) > MAX_CHARS:
            text = text[:MAX_CHARS] + f"\n\n[... File truncated at {MAX_CHARS} characters ...]"

        file_size = response["ContentLength"]
        content_type = response.get("ContentType", "unknown")

        return (
            f"[S3 Document Retrieved Successfully]\n"
            f"Bucket: {bucket}\n"
            f"Key: {key}\n"
            f"Size: {file_size:,} bytes | Type: {content_type}\n"
            f"{'=' * 50}\n"
            f"{text}"
        )

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchBucket":
            return f"Error: Bucket '{bucket}' does not exist or you don't have access."
        elif error_code == "NoSuchKey":
            return f"Error: File '{key}' not found in bucket '{bucket}'."
        elif error_code == "AccessDenied":
            return f"Error: Access denied. Check your IAM permissions for s3:GetObject on {bucket}/{key}."
        else:
            return f"S3 Error ({error_code}): {e.response['Error']['Message']}"

    except NoCredentialsError:
        return "Error: No AWS credentials found. Configure credentials with 'aws configure' or environment variables."

    except Exception as e:
        return f"Unexpected error reading S3 document: {str(e)}"


@tool
def list_s3_objects(bucket: str, prefix: str = "") -> str:
    """
    List files available in an S3 bucket (optionally filtered by prefix/folder).

    Use this tool when the user wants to see what documents are available
    in their S3 bucket before reading one, or when they reference a folder
    rather than a specific file.

    Args:
        bucket: The S3 bucket name
        prefix: Optional folder prefix to filter results (e.g., 'reports/2024/')

    Returns:
        A formatted list of object keys and their sizes.
    """
    s3 = boto3.client("s3")

    try:
        kwargs = {"Bucket": bucket, "MaxKeys": 50}
        if prefix:
            kwargs["Prefix"] = prefix

        response = s3.list_objects_v2(**kwargs)

        if response.get("KeyCount", 0) == 0:
            return f"No files found in s3://{bucket}/{prefix}"

        objects = response.get("Contents", [])
        lines = [f"Files in s3://{bucket}/{prefix or ''} ({len(objects)} items):\n"]

        for obj in objects:
            size_kb = obj["Size"] / 1024
            lines.append(f"  • {obj['Key']}  ({size_kb:.1f} KB)")

        if response.get("IsTruncated"):
            lines.append(f"\n  [Results limited to 50 — more files exist]")

        return "\n".join(lines)

    except ClientError as e:
        error_code = e.response["Error"]["Code"]
        if error_code == "NoSuchBucket":
            return f"Error: Bucket '{bucket}' does not exist."
        elif error_code == "AccessDenied":
            return f"Error: Access denied to bucket '{bucket}'. Check your IAM permissions."
        else:
            return f"S3 Error ({error_code}): {e.response['Error']['Message']}"

    except NoCredentialsError:
        return "Error: No AWS credentials found. Run 'aws configure' first."

    except Exception as e:
        return f"Unexpected error listing S3 objects: {str(e)}"
