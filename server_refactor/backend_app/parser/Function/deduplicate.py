import os
import sqlite3
import pandas as pd
from sqlalchemy import create_engine

def deduplicate(command):
    response = {'text': ""}
    command_parts = command
    table_name = command_parts[command_parts.index("FROM") + 1].split(';')[0]
    feature = command_parts[command_parts.index("INSPECT") + 1]
    connection_string = os.getenv("POSTGES_URL")
    query = f'SELECT * FROM "{table_name}"'
    conn = create_engine(connection_string)
    data = pd.read_sql_query(query, conn)

    if feature!='*':
        if feature in data.columns:
            data.drop_duplicates(subset=[feature], inplace=True)
            data.to_sql(table_name, conn, if_exists='replace', index=False)
            response['text'] = f"Deduplication based on feature '{feature}' complete."
        else:
            response['text'] = f"Feature '{feature}' not found in the table."

    else:
        initial_rows = len(data)
        data.drop_duplicates(inplace=True)
        final_rows = len(data)
        print(final_rows, initial_rows)
        if final_rows < initial_rows:
            data.to_sql(table_name, conn, if_exists='replace', index=False)
            response['text'] = "Deduplication based on all features complete."
        else:
            response['text'] = "No duplicate rows found."
    return response


