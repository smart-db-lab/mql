import os
from sqlalchemy import text
from ..Function.utility import db_engine

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
            conn = db_engine()

            tables = [dataset_name]
            
            with conn.connect() as connection:
                for table_name in tables:
                    try:
                        connection.execute(text(f'DROP TABLE IF EXISTS "{table_name}";'))
                    except Exception as drop_error:
                        print(f"Failed to drop table {table_name}: {str(drop_error)}")
                        response['text'] = f"Failed to drop table {table_name}: {str(drop_error)}"
                        return response
                    finally:
                        connection.commit()
            if os.path.exists(dataset_path):
                os.remove(dataset_path)
            return {"text": f"Dataset '{dataset_name}' has been successfully dropped, and all tables removed."}

        else:
            return {"text": "Invalid command. Use: DROP DATASET dataset_name;"}
    except Exception as e:
        return {"text": f"An error occurred: {str(e)}"}
    