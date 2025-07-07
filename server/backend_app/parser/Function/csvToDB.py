# server/backend_app/parser/Function/csvToDB.py

import os
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

class CSVToDBError(Exception):
    pass

def csv_to_db(csv_file, user_id=None,csv_name=None):
    """
    Converts a CSV file to a PostgreSQL table.
    Args:
        csv_file: file-like object or file path
        user_id: (optional) for per-user table naming
    Returns:
        table_name (str)
    Raises:
        CSVToDBError
    """
    connection_string = os.getenv("POSTGRES_URL")
    if not connection_string:
        raise CSVToDBError("POSTGRES_URL environment variable not set.")

    try:
        if hasattr(csv_file, 'read'):
            file_name, _ = os.path.splitext(csv_file.name)
            df = pd.read_csv(csv_file)
        else:
            file_name, _ = os.path.splitext(os.path.basename(csv_file))
            df = pd.read_csv(csv_file)

        # table_name = f"{user_id}_{file_name}" if user_id else file_name
        # table_name = table_name[:63]  # PostgreSQL table name limit
        table_name = csv_name.split('.')[0]
        print(table_name)
        engine = create_engine(connection_string)
        df.to_sql(table_name, engine, index=False, if_exists='replace')

        return table_name
    except FileNotFoundError:
        raise CSVToDBError(f"File '{csv_file}' does not exist.")
    except pd.errors.EmptyDataError:
        raise CSVToDBError(f"File '{csv_file}' is empty or invalid.")
    except psycopg2.OperationalError as e:
        raise CSVToDBError(f"Database connection error: {e}")
    except Exception as e:
        raise CSVToDBError(f"Unexpected error: {e}")