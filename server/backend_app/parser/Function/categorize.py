import sqlite3
import pandas as pd
from sqlalchemy import text
import os
from .utility import response_schema, db_engine
from ..operation.utils import get_arg
def categorize(table_name,cmd):
    feature = get_arg(cmd, "INSPECT", "")
    labels = [cat for cat in get_arg(cmd, "INTO", "").split(',')]
    # print(labels, feature)
    response = response_schema()
    query = text(f'SELECT * FROM "{table_name}"')
    conn = db_engine()
    df=  pd.read_sql(query,conn)
    df=pd.DataFrame(df)
    min_value = df[feature].min()
    max_value = df[feature].max()
    num_groups = len(labels)
    col_range = (max_value - min_value + 1) / num_groups
    # print("res ",col_range)
    col_ranges = [(min_value + i * col_range , min_value + (i + 1) * col_range) for i in range(num_groups)] # min_value + (i + 1) * col_range -1 will be like (1,2) (3,4)
    col_ranges[-1] = (col_ranges[-1][0], max_value)
    # labels = [f"{label_prefix}-{i+1}" for i in range(num_groups)]
    # print(col_ranges)
    def assign_label(age):
        for i, (start, end) in enumerate(col_ranges):
            # print(start,end,age)
            if start <= age <= end:
                return labels[i]
        return 'Unknown'

    df['Category'] = df[feature].apply(assign_label)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    response['text'].append(f"Categorize Done!")
    return response

# min_value=5
# max_value=100
# num_groups=4
# col_range = (max_value - min_value + 1) / num_groups

# col_ranges = [(min_value + i * col_range , min_value + (i + 1) * col_range) for i in range(num_groups)] # min_value + (i + 1) * col_range -1 will be like (1,2) (3,4)