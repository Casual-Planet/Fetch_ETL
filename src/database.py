import psycopg2
from psycopg2.extras import DictCursor

def connect_to_db():
    """
    Establishes a connection to the PostgreSQL database.

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
    Inserts the provided data into the 'user_logins' table in the database.

    :param conn: Database connection object.
    :param data: Dictionary containing user login data.
    """
    try:
        # Use a dictionary cursor to facilitate the parameterized query execution
        with conn.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(
                """
                INSERT INTO user_logins (user_id, device_type, masked_ip, masked_device_id, locale, app_version)
                VALUES (%(user_id)s, %(device_type)s, %(masked_ip)s, %(masked_device_id)s, %(locale)s, %(app_version)s);
                """,
                data,
            )
        conn.commit()  # Commit the transaction to make the changes permanent
    except Exception as e:
        # Print the error message if insertion fails
        print(f"Error inserting data into the database: {e}")
