import pandas as pd
import os
import sqlite3

from ..Function.categorize import categorize

from ..Function.deduplicate import deduplicate
from ..Function.encoding import encoding
from ..Function.checknull import checknull


def inspect(command):
    '''
            INSPECT CHECKNULL FEATURES medv FROM Boston
            INSPECT ENCODING USING ONE-HOT ENCODING feature medv from boston

    '''
    command_parts = [part for part in command.split(" ") if part.strip()]
    print(command_parts)
    try:
        operation_types = ["CHECKNULL", "ENCODING","DEDUPLICATE","CATEGORIZE"]
        operation_type = next((word for word in operation_types if word in command), "") 
        dataset_name = command_parts[command_parts.index("FROM") + 1].split(';')[0]
        features=command_parts[command_parts.index("INSPECT") + 1] #.split(',')
          
    except:
        pass
    response = {'text': [], 'graph': '', 'table': '', 'query': command}
    # url = os.path.join(os.path.dirname(__file__), f"../../data/files/{dataset_name}.db")
    if operation_type.upper()=="CHECKNULL":
        response = checknull(dataset_name)
        return response
    elif operation_type.upper() =="ENCODING":
        res=encoding(dataset_name,command_parts)
        if res: return res
        else:
            response['text'].append("Something wrong. try again")
            return response
    elif operation_type.upper() =="DEDUPLICATE":
        res= deduplicate(command_parts)
        if res:
            return res
        else:
            response['text'].append("Something wrong. try again")
            return response
    elif operation_type.upper() =="CATEGORIZE":
        res = categorize(dataset_name,command_parts)
        if res:
            return res
        else:
            response['text'].append("Something wrong. try again")

    # conn = sqlite3.connect(url)
    # query = f"SELECT * FROM {dataset_name}"
    # df = pd.read_sql_query(query, conn)
