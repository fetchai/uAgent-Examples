import psycopg2
from psycopg2 import OperationalError


def create_connection(dbname, user, password, host="localhost", port="5432"):
    """
    Create a connection to the PostgreSQL database.

    :param dbname: Name of the database
    :param user: Database user
    :param password: User's password
    :param host: Database host
    :param port: Database port
    :return: Connection object or None if connection fails
    """
    try:
        conn = psycopg2.connect(
            dbname=dbname, user=user, password=password, host=host, port=port
        )
        print("Connection successful")
        return conn
    except OperationalError as error:
        print(f"Error connecting to PostgreSQL database: {error}")
        return None


def close_connection(conn):
    if conn:
        conn.close()
        print("Connection closed")
