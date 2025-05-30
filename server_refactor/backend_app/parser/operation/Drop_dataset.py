import os
import sqlite3
from sklearn.preprocessing import OneHotEncoder, OrdinalEncoder, LabelEncoder
from sqlalchemy import create_engine
def drop_dataset(command):
    """
    DROP DATASET dataset_name;
    """
    command_parts = [part for part in command.split(" ") if part.strip()]
    print(command_parts)
    try:
        if command_parts[0].upper() == "DROP" and command_parts[1].upper() == "DATASET":
            dataset_name = command_parts[2].split(';')[0]
            dataset_path = os.path.join(os.path.dirname(__file__), f"../../data/files/{dataset_name}.db")
            
            connection_string = os.getenv("POSTGES_URL")
            conn = create_engine(connection_string).raw_connection()
            cursor = conn.cursor()

            tables = [dataset_name]
            
            # Drop all tables
            for table_name in tables:
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS \"{table_name}\";")
                    conn.commit()  # Explicitly commit after each DROP TABLE
                except Exception as drop_error:
                    print(f"Failed to drop table {table_name}: {str(drop_error)}")
            conn.commit()
            cursor.close()
            conn.close()
            if os.path.exists(dataset_path):
                os.remove(dataset_path)
            return {"text": f"Dataset '{dataset_name}' has been successfully dropped, and all tables removed."}

        else:
            return {"text": "Invalid command. Use: DROP DATASET dataset_name;"}
    except Exception as e:
        return {"text": f"An error occurred: {str(e)}"}