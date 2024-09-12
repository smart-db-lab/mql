import os

import pandas as pd
import sqlite3
from sqlalchemy import create_engine
import psycopg2

def csvToDB(csv_file):
    connection_string = os.getenv("POSTGES_URL")
    try:
        df = pd.read_csv(csv_file)

        file_name, _ = os.path.splitext(csv_file.name)

        column_data_types = {column: 'TEXT' for column in df.columns}

        conn = psycopg2.connect(connection_string)
        engine = create_engine(connection_string)

        # Write the DataFrame to the database using the engine
        df.to_sql(file_name, engine, index=False, if_exists='replace')

        conn.commit()
        conn.close()

        print("CSV dataset successfully converted to PostgreSQL table.")
    except :
        print("error while csv to database")
