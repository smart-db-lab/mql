from .utility import db_engine
from sqlalchemy import text


def checknull(table_name):
    try:
        response = {'text': [], 'graph': '', 'table': ''}
        conn = db_engine()
        
        with conn.connect() as connection:
            column_query = text(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}';")
            column_names = [row[0] for row in connection.execute(column_query).fetchall()]
            print(column_names)
            
            data_query = text(f'SELECT * FROM "{table_name}"')
            rows = connection.execute(data_query).fetchall()
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
        return response
    except Exception as e:
        response['text']= f"Error occurred: {e}"
        return response




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
            