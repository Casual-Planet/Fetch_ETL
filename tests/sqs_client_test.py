import unittest
from unittest.mock import patch, Mock
from src.sqs_client import create_sqs_client, get_messages_from_queue, delete_message

class TestSQSClientFunctions(unittest.TestCase):

    @patch('sqs_client.boto3.Session')
    def test_create_sqs_client(self, mock_session):
        mock_client = Mock()
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.client.return_value = mock_client

        result = create_sqs_client()

        mock_session.assert_called_once()
        mock_session_instance.client.assert_called_once_with('sqs', endpoint_url='http://localhost:4566')
        self.assertEqual(result, mock_client)

    @patch('sqs_client.create_sqs_client')
    def test_get_messages_from_queue(self, mock_create_sqs_client):
        mock_client = Mock()
        mock_create_sqs_client.return_value = mock_client
        mock_response = {
            'Messages': [
                {'Body': 'TestMessage1', 'ReceiptHandle': 'TestReceipt1'},
                {'Body': 'TestMessage2', 'ReceiptHandle': 'TestReceipt2'}
            ]
        }
        mock_client.receive_message.return_value = mock_response

        result = get_messages_from_queue(mock_client, "test_url")

        self.assertEqual(result, mock_response['Messages'])

    @patch('sqs_client.create_sqs_client')
    def test_delete_message(self, mock_create_sqs_client):
        mock_client = Mock()
        mock_create_sqs_client.return_value = mock_client

        delete_message(mock_client, "test_url", "test_receipt")

        mock_client.delete_message.assert_called_once_with(QueueUrl="test_url", ReceiptHandle="test_receipt")

if __name__ == "__main__":
    unittest.main()
