import os
import psycopg2
from dotenv import load_dotenv

load_dotenv(dotenv_path="Task1/.env")

def get_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )
    conn.autocommit = True
    return conn


def get_cursor(conn):
    return conn.cursor()
