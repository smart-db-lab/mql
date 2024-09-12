import os

import pandas as pd
import psycopg2
from sqlalchemy import create_engine


def Query_manipulate(query):
    response={}
    print(query)
    query=query.replace('\n', '').replace('\r', '')
    try:
        connection_string = os.getenv("POSTGES_URL")
        conn = create_engine(connection_string)
        if query.strip().upper().startswith("SELECT"):
            # Execute DQL query
            with conn.connect():
                df=pd.read_sql_query(query, conn)
                response['table'] = df.to_dict(orient="records")
                return response
        else:
            # Execute DDL or DML query
            # connection_string = os.getenv("DATABASE_URL")
            # conn = create_engine(connection_string)
            postgres_url = os.getenv("POSTGES_URL")
            conn = psycopg2.connect(postgres_url)
            # conn = connection.cursor()
            with conn.cursor() as connection:
                result = connection.execute(query)
                if result.returns_rows:
                    df=pd.DataFrame(result.fetchall(), columns=result.keys())
                    response['table'] = df.to_dict(orient="records")
                    return response
                else:
                    response['text']= "Query executed successfully"
                    return response
    except Exception as e:
        response['text']=f"Error occurred: {e}"
        print (f"error {e}")
        return response