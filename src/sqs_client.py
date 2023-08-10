import boto3
from botocore.exceptions import NoCredentialsError


def create_sqs_client():
    """Initialize and return a local SQS client."""
    session = boto3.Session()
    return session.client('sqs', endpoint_url='http://localhost:4566')


def get_messages_from_queue(client, queue_url):
    """
    Fetch up to 10 messages from the specified SQS queue.

    Args:
    - client: The SQS client instance.
    - queue_url: URL of the SQS queue.

    Returns:
    - List of messages or empty list if none/error.
    """
    try:
        response = client.receive_message(QueueUrl=queue_url, MaxNumberOfMessages=10)
        return response.get('Messages', [])
    except NoCredentialsError:
        print("No AWS credentials found.")
        return []


def delete_message(client, queue_url, receipt_handle):
    """Remove a message from the queue using its receipt handle."""
    client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
