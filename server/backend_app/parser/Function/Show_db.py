import os,psycopg2
import pandas as pd
from sqlalchemy import create_engine

def show_db(data):
    splitted_data = data.split()
    table_name = splitted_data[1].split(';')[0]
    connection_string = os.getenv("POSTGES_URL")
    query = f'SELECT * FROM "{table_name}"'
    engine = create_engine(connection_string)
    data = pd.read_sql_query(query,engine)
    conn = psycopg2.connect(connection_string)
    response={}
    response['table']=data.to_dict(orient="records")
    return response