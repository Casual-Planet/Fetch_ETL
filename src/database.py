import psycopg2
from psycopg2.extras import DictCursor


def connect_to_db():
    """
    Connects to the PostgreSQL database.

    :return: Database connection object.
    """
    return psycopg2.connect(
        host="localhost",
        port="5432",
        dbname="postgres",
        user="postgres",
        password="postgres"
    )


def insert_into_db(conn, data):
    """
    Inserts the provided data into the 'user_logins' table in the PostgreSQL database.

    :param conn: Database connection object.
    :param data: Dictionary containing user login data.
    """
    cursor = conn.cursor(cursor_factory=DictCursor)
    cursor.execute(
        """
        INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version)
        VALUES (%(user_id)s, %(device_type)s, %(masked_ip)s, %(masked_device_id)s, %(locale)s, %(app_version)s);
        """,
        data,
    )
    conn.commit()
