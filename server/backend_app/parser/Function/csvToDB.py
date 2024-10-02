import os
import pandas as pd
from sqlalchemy import create_engine
import psycopg2

def csvToDB(csv_file):
    """
    Converts the provided CSV file to a PostgreSQL table using the connection string
    defined in the POSTGRES_URL environment variable.

    Handles both file-like objects (uploaded from frontend) and file paths (from server-side folder).
    """    
    connection_string = os.getenv("POSTGES_URL")

    if not connection_string:
        print("Connection string is missing. Please set the POSTGRES_URL environment variable.")
        return

    try:        
        if hasattr(csv_file, 'read'):            
            file_name, _ = os.path.splitext(csv_file.name)            
            df = pd.read_csv(csv_file)
        else:            
            file_name, _ = os.path.splitext(os.path.basename(csv_file))            
            df = pd.read_csv(csv_file)
        
        file_name = file_name[:63]
        
        engine = create_engine(connection_string)
        
        df.to_sql(file_name, engine, index=False, if_exists='replace')

        print(f"CSV dataset successfully converted to PostgreSQL table: {file_name}")
    except FileNotFoundError:
        print(f"Error: The file '{csv_file}' does not exist.")
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{csv_file}' is empty or invalid.")
    except psycopg2.OperationalError as e:
        print(f"Database connection error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while converting CSV to database: {e}")
