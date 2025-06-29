import base64
import io
import json
import sqlite3
import uuid
import pandas as pd
import numpy as np
import os
from sqlalchemy import create_engine
import category_encoders as ce
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.svm import SVR, SVC
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
import matplotlib.pyplot as plt
import seaborn as sns
import dill
from tpot import TPOTRegressor, TPOTClassifier

from ..Function.select_algorithm import select_algorithm


def construct(command,user=None):
    command_parts = [part for part in command.split(" ") if part.strip()]
    command_parts_upper = [part.upper() for part in command_parts]  # Convert command parts to uppercase

    operation_types = ["PREDICTION", "CLASSIFICATION", "CLUSTERING"]

    operation_type = command_parts[command_parts_upper.index("FOR") + 1]
    dataset_train_name = command_parts[command_parts_upper.index("FROM") + 1].split(';')[0]
    model_name = command_parts[command_parts_upper.index("CONSTRUCT") + 1]

    if "ALGORITHM" in command_parts_upper:
        algorithm_name = command_parts[command_parts_upper.index("ALGORITHM")+ 1] 
    else :
        algorithm_name='AUTO_ML'

    # features = command_parts[command_parts_upper.index("FEATURES") + 1].split(',')    
    
    connection_string = os.getenv("POSTGES_URL")
    query = f'SELECT * FROM "{dataset_train_name}"'
    conn = create_engine(connection_string)

    df = pd.read_sql_query(query, conn)
    feature_part=command_parts[[part.upper() for part in command_parts].index("FEATURES") + 1].strip()
    features= df.columns.tolist() if '*' in feature_part else feature_part.split(',') 

    X = df[features]
    y = None

    global model, accuracy, label_name, response
    response = {'text': [], 'graph': '', 'table': ''}
    model = None 
    accuracy = None

    if operation_type != "CLUSTERING":
        target = command_parts[command_parts_upper.index("TARGET") + 1]
        y = df[target]

    if y is not None and operation_type.upper() != "CLUSTERING":
        test_s = float(command_parts[command_parts_upper.index("TEST") + 2]) if "TEST" in command_parts_upper else 20
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size= test_s/100, random_state=42)
        model = select_algorithm(operation_type, algorithm_name.upper())
        if not algorithm_name:   algorithm_name='AUTO_ML'
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        try:
            url = os.path.join(os.path.dirname(__file__), f"../model/{model_name}.pkl")
            with open(url, 'wb') as file:
                pickle.dump(model, file)
                response['text'].append( f"Model {model_name} is created by algorithm {algorithm_name} as name {model_name}.pkl. ")
        except:
            url = os.path.join(os.path.dirname(__file__), f"../model/{model_name}.dill")
            with open(url, 'wb') as file:
                dill.dump(model, file)
                response['text'].append( f"Model {model_name} is created by algorithm {algorithm_name} as name {model_name}.dill. ")
        if "TPOT" in str(model): 
            response['text'].append( f"{json.dumps( str(model.fitted_pipeline_.steps[0]))}. ")
        if operation_type.upper() == "CLASSIFICATION" :
            accuracy = accuracy_score(y_test, y_pred)*100
            response['text'].append( f"Accuracy of model {model_name} is {accuracy} .")
            print(response['text'])
        elif operation_type.upper() == "PREDICTION":
            accuracy = r2_score(y_test, y_pred)*100
            response['text'].append( f"R-squared value of model {model_name} is {accuracy} .")
            print("R^2 Score:", accuracy)
  
    else:
        n_cluster = command_parts[command_parts_upper.index("CLUSTER")+2] if "CLUSTER"  in command_parts_upper else 3
        if algorithm_name == 'default':
            algorithm_name = KMeans
        model = select_algorithm(operation_type, algorithm_name.upper(), n_clusters=n_cluster)
        X = pd.DataFrame(X.select_dtypes(include=[np.number]))
        model.fit(X)
        try:
            url = os.path.join(os.path.dirname(__file__), f"../model/{model_name}.pkl")
            with open(url, 'wb') as file:
                pickle.dump(model, file)
                response['text'].append(f"Model {model_name} is created by algorithm {algorithm_name} as name {model_name}.pkl. ")
        except:
            url = os.path.join(os.path.dirname(__file__), f"../model/{model_name}.dill")
            with open(url, 'wb') as file:
                dill.dump(model, file)
            response['text'].append( f"Model {model_name} is created by algorithm {algorithm_name} as name {model_name}.dill. ")

    return response
