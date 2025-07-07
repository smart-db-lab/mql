import os
import sqlite3
import pandas as pd
from sklearn.impute import SimpleImputer
from sqlalchemy import create_engine,text
from .utility import response_schema,db_engine
def impute(table_name,command_parts):
    """Impute missing values in a dataset based on the provided command. """
    response = {'text': []}
    # command_parts = [part for part in command.split(" ") if part.strip()]
    # table_name = command_parts[command_parts.index("FROM") + 1].split(';')[0]
    features = command_parts[command_parts.index("IMPUTE") - 1]
    strat = command_parts[command_parts.index("STRATEGY") + 1] if "STRATEGY" in command_parts else "mean"
    query = text(f'SELECT * FROM "{table_name}"')
    print(query)
    conn = db_engine()
    data = pd.read_sql_query(query, conn)
    numerical_cols = data.select_dtypes(include=['number']).columns
    categorical_cols = data.select_dtypes(include=['object']).columns
    print(features)
    flag=0
    if features == '*':
        if data.isnull().any().any():  # Check if any null values exist
            try:
                numerical_imputer = SimpleImputer(strategy=strat.lower())
                data[numerical_cols] = numerical_imputer.fit_transform(data[numerical_cols])
                flag=1
            # except Exception as e:
            #     # response['text'].append( f"Error occurred: {e}")
            # try:
                categorical_imputer = SimpleImputer(strategy=strat.lower())
                data[categorical_cols] = categorical_imputer.fit_transform(data[categorical_cols])
                flag=1
            except Exception as e:
                print(f"Error occurred: {e}")
                pass
                # response['text'].append(f"Error occurred: {e}")
        else:
            response['text'].append("No missing values to impute.")
            return response

    
    elif features:
        if features in numerical_cols:
            if data[features].isnull().any(): 
                numerical_imputer = SimpleImputer(strategy=strat.lower())
                data[features] = numerical_imputer.fit_transform(data[[features]])
                flag=1
            else:
                response['text'].append(f"No missing values in {features} .")
                return response
        elif features in categorical_cols:
            if data[features].isnull().any():
                categorical_imputer = SimpleImputer(strategy=strat.lower())
                data[features] = categorical_imputer.fit_transform(data[[features]]).ravel()
                flag=1
            else:
                response['text'].append(f"No missing values in {features}.")
                return response
        else:
            response['text'].append(f"{features} not exists in {table_name}")
            return response
    data.to_sql(table_name, conn, if_exists='replace', index=False)
    
    if flag:
        response['text'].append("Imputation complete")
    return response
