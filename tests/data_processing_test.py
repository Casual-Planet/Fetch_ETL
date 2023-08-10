import unittest
from unittest.mock import MagicMock
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
    def test_insert_into_db(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        data = {
            'user_id': '424cdd21-063a-43a7-b91b-7ca1a833afae',
            'device_type': 'android',
            'masked_ip': '199.172.111.135',
            'masked_device_id': '593-47-5928',
            'locale': 'RU',
            'app_version': 230  # updated according to changes
        }
        insert_into_db(mock_conn, data)
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()

if __name__ == "__main__":
    unittest.main()
