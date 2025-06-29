import os
import psycopg2
from sqlalchemy import create_engine, text

def db_engine():
    conn = create_engine(os.getenv("POSTGRES_URL"))
    print(conn, "connection engine")
    return conn

def response_schema():
    response = {'text': [], 'graph': '', 'table': ''}
    return response