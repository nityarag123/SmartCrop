# db.py (PyMySQL)
import pymysql
import os
from config import Config

def get_conn():
    try:
        db_host = os.getenv('DB_HOST', 'localhost')
        db_port = int(os.getenv('DB_PORT', '3306'))
        return pymysql.connect(
            host=db_host,
            port=db_port,
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASSWORD') or None,
            database=os.getenv('DB_NAME', 'smartcrop'),
            cursorclass=pymysql.cursors.DictCursor
        )
    except pymysql.err.OperationalError as e:
        raise Exception(
            f"Database connection failed: {e}. Ensure MySQL is running and that "
            "DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, and DB_NAME in .env are correct."
        ) from e

def close_conn(conn):
    if conn:
        conn.close()
