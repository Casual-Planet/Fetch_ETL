import json
from sqs_client import create_sqs_client, get_message_from_queue
from data_processing import mask_data, flatten_json
from database import connect_to_db, insert_into_db

def main():
    """
    The main function that orchestrates the ETL process.
    """
    # Create an SQS client
    sqs_client = create_sqs_client()

    # Connect to the PostgreSQL database
    conn = connect_to_db()

    # Retrieve a message from the SQS queue
    message = get_message_from_queue(sqs_client, 'http://localhost:4566/000000000000/login-queue')
    if message is not None:
        # Parse the original JSON body from the message
        original_body = json.loads(message['Body'])

        # Mask sensitive data in the JSON body
        masked_data = mask_data(original_body)

        # Flatten the masked JSON data
        flat_data = flatten_json(masked_data)

        # Insert the flattened data into the PostgreSQL database
        insert_into_db(conn, flat_data)

if __name__ == "__main__":
    main()
