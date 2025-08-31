import os

import pandas as pd
import psycopg2
from sqlalchemy import create_engine
from ..Function.utility import db_engine, response_schema

def Query_manipulate(query):
    response= response_schema()
    print(query)
    query=query.replace('\n', '').replace('\r', '')
    try:
        connection_string = os.getenv("POSTGRES_URL")
        conn = create_engine(connection_string)
        if query.strip().upper().startswith("SELECT"):
            # Execute DQL query
            with conn.connect():
                df=pd.read_sql_query(query, conn)
                response['table'] = df.to_dict(orient="records")
                # print(response)
                return response
        else:
            # Execute DDL or DML query
            postgres_url = os.getenv("POSTGRES_URL")
            conn = psycopg2.connect(postgres_url)
            # conn = connection.cursor()
            with conn.cursor() as connection:
                result = connection.execute(query)
                conn.commit()
                if result and  result.returns_rows:
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