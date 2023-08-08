import unittest
from unittest.mock import MagicMock, Mock
from psycopg2.extras import DictCursor
from src.database import  insert_into_db

class TestDatabase(unittest.TestCase):
    def test_insert_into_db(self):
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        data = {'user_id': '424cdd21-063a-43a7-b91b-7ca1a833afae', 'device_type': 'android', 'masked_ip': '199.172.111.135', 'masked_device_id': '593-47-5928', 'locale': 'RU', 'app_version': '2.3.0'}
        insert_into_db(mock_conn, data)
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
