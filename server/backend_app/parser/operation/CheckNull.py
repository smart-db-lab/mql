from sqlalchemy import create_engine
import os
def check_null_values_in_db(db_file, table_name):
    global response
    # connection = sqlite3.connect(db_file)
    connection_string = os.getenv("POSTGES_URL")
    query = f'SELECT * FROM "{table_name}"'
    conn = create_engine(connection_string)
    cursor = conn.cursor()

    # Get column names
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns_info = cursor.fetchall()
    column_names = [col_info[1] for col_info in columns_info]
    print(column_names)

    # Fetch all rows
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    u = 1

    # Check for null values in each column
    for column_name in column_names:
        null_rows = [row for row in rows if row[column_names.index(column_name)] is None]
        if null_rows and u:
            response = ["null value exist in column ", " : "]
            u = 0
        if null_rows:
            print(f"Null values found in {column_name} column:")
            response.append(f" {column_name},")
            for row in null_rows:
                print(row)
        else:
            print(f" in {column_name} column.")
    if u:
        response.append(f"No null values found {table_name}")

    conn.close()
