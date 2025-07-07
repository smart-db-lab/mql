import os
import psycopg2
from sqlalchemy import create_engine, text

def db_engine():
    try:
        conn = create_engine(os.getenv("POSTGRES_URL"))
    except Exception as e:
        print(f"Error creating database engine: {e}")
        raise Exception(f"Database connection failed.{e}")
    print(conn, "connection engine")
    return conn

def response_schema():
    response = {'text': [], 'graph': '', 'table': ''}
    return response