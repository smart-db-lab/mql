import os,psycopg2
import pandas as pd
from sqlalchemy import text
from .utility import db_engine,response_schema
def show_db(data):
    splitted_data = data.split()
    table_name = splitted_data[1].split(';')[0]
    query = text(f'SELECT * FROM "{table_name}"')
    conn = db_engine()
    data = pd.read_sql_query(query,conn)
    response = response_schema()
    response['table']=data.to_dict(orient="records")
    return response