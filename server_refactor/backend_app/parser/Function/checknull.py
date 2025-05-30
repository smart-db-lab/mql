import os
import psycopg2

def checknull(table_name):
    try:
        response = {'text': [], 'graph': '', 'table': ''}
        postgres_url = os.getenv("POSTGES_URL")
        connection = psycopg2.connect(postgres_url)
        cursor = connection.cursor()
        
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
        column_names = [row[0] for row in cursor.fetchall()]
        print(column_names)
        cursor.execute(f'SELECT * FROM "{table_name}"')
        rows = cursor.fetchall()
        u = 1
        for column_name in column_names:
            null_rows = [row for row in rows if row[column_names.index(column_name)] is None]
            if null_rows and u:
                response['text'].append(["null value exist in column ", " : "])
                u = 0
            if null_rows:
                print(f"  Null values found in {column_name} column:")
                response['text'].append(f" {column_name},")
                for row in null_rows:
                    print(row)
            else:
                print(f" in {column_name} column.")
        if u:
            response['text'].append(f"No null values found in {table_name}")
        cursor.close()
        return response
    except Exception as e:
        return f"Error occurred: {e}"




#   # Create engine
#         engine = create_engine(postgres_url)
        
#         with engine.connect() as connection:
#             query = text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
#             column_names = [row[0] for row in connection.execute(query).fetchall()]

#         response = []

#         for column_name in column_names:
#             with engine.connect() as connection:
#                 query = text(f"SELECT * FROM {table_name} WHERE \"{column_name}\" IS NULL;")
#                 null_rows = connection.execute(query).fetchall()
            