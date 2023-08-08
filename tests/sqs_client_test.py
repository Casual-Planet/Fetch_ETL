import unittest
from unittest.mock import MagicMock
from src.sqs_client import create_sqs_client, get_message_from_queue
from botocore.exceptions import NoCredentialsError

class TestSQSClient(unittest.TestCase):

    def test_get_message_from_queue(self):
        mock_client = MagicMock()
        mock_client.receive_message.return_value = {'Messages': [{'message': 'Hello'}]}
        result = get_message_from_queue(mock_client, 'queue_url')
        self.assertEqual(result, {'message': 'Hello'})

    def test_no_credentials(self):
        mock_client = MagicMock()
        mock_client.receive_message.side_effect = NoCredentialsError()
        result = get_message_from_queue(mock_client, 'queue_url')
        self.assertIsNone(result)
