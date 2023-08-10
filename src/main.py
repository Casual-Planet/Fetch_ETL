from data_processing import mask_data, flatten_json
from database import connect_to_db, insert_into_db
from sqs_client import create_sqs_client, get_messages_from_queue, delete_message


def main():
    """
    Main function to process messages from an SQS queue, transform and mask data,
    then insert into a PostgreSQL database.
    """
    # Establish a connection to the database
    conn = connect_to_db()

    # Create an SQS client
    sqs_client = create_sqs_client()

    # Define the SQS queue URL
    queue_url = "http://localhost:4566/000000000000/login-queue"

    # Continuously fetch messages from the SQS queue until it's empty
    messages = get_messages_from_queue(sqs_client, queue_url)
    while messages:
        for message in messages:
            body = message['Body']

            # Transform and mask the data before insertion
            processed_data = flatten_json(mask_data(body))

            # Insert the processed data into the database
            insert_into_db(conn, processed_data)

            # Delete the processed message from the SQS queue
            delete_message(sqs_client, queue_url, message['ReceiptHandle'])

        # Fetch the next batch of messages
        messages = get_messages_from_queue(sqs_client, queue_url)

    # Close the database connection
    conn.close()


if __name__ == "__main__":
    main()
