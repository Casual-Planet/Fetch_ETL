import unittest
from unittest.mock import patch, Mock
import psycopg2
from src.data_processing import mask_data, flatten_json, encrypt_data, decrypt_data
from src.database import insert_into_db


class TestDataProcessing(unittest.TestCase):

    def setUp(self):
        self.original_data = {
            'user_id': '424cdd21-063a-43a7-b91b-7ca1a833afae',
            'app_version': '2.3.0',
            'device_type': 'android',
            'ip': '199.172.111.135',
            'locale': 'RU',
            'device_id': '593-47-5928'
        }

    def test_mask_data(self):
        masked_data = mask_data(self.original_data.copy())
        self.assertNotEqual(masked_data['ip'], self.original_data['ip'])
        self.assertNotEqual(masked_data['device_id'], self.original_data['device_id'])

    def test_flatten_json(self):
        masked_data = mask_data(self.original_data.copy())
        flattened_data = flatten_json(masked_data)
        self.assertEqual(flattened_data['masked_ip'], masked_data['ip'])
        self.assertEqual(flattened_data['masked_device_id'], masked_data['device_id'])

    def test_encryption_decryption(self):
        original_string = "TestString"
        encrypted_data = encrypt_data(original_string)
        decrypted_data = decrypt_data(encrypted_data)
        self.assertEqual(original_string, decrypted_data)

    @patch('database.psycopg2.connect')
    def test_insert_into_db(self, mock_connect):
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor

        flattened_data = flatten_json(self.original_data.copy())
        insert_into_db(mock_connection, flattened_data)

        mock_cursor.execute.assert_called_once()
        mock_connection.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
