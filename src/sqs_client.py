import boto3
from botocore.exceptions import NoCredentialsError

def create_sqs_client():
    """
    Creates an SQS client using the boto3 library.
    :return: SQS client object.
    """
    session = boto3.Session()
    return session.client('sqs', endpoint_url='http://localhost:4566')

def get_message_from_queue(client, queue_url):
    """
    Retrieves a message from the SQS queue using the SQS client.
    :param client: SQS client object.
    :param queue_url: URL of the SQS queue to retrieve messages from.
    :return: A dictionary containing the retrieved message, or None if no messages are found.
    """
    try:
        messages = client.receive_message(QueueUrl=queue_url)
        if 'Messages' in messages:
            return messages['Messages'][0]
    except NoCredentialsError:
        print("No AWS credentials found.")
        return None
