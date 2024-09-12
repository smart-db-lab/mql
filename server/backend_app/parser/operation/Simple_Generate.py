import base64
import io
import json
import sqlite3
import uuid
import matplotlib
import pandas as pd
import numpy as np
import os
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
import sqlalchemy
from sympy import plot
from ..Function.display_result import display_results
from ..Function.select_algorithm import select_algorithm
from sqlalchemy import create_engine
import dill
from tpot import TPOTRegressor, TPOTClassifier
matplotlib.use('Agg')

def load_over_df(df_name):
    url = os.path.join(os.path.dirname(__file__), f"../../data/files/{df_name}.csv")
    return pd.read_csv(url)

def load_saved_model(model_name):
    url = os.path.join(os.path.dirname(__file__), f"../model/{model_name}.pkl")
    try:
        with open(url, 'rb') as file:
            model = pickle.load(file)
    except:
        response["text"] = f"Model: [{model_name}] Not found."
        return model,response

def simple_generate(command):  
    command_parts = [part for part in command.split(" ") if part.strip()]
    try:
        operation_types = ["PREDICTION", "CLASSIFICATION", "CLUSTERING"]
        operation_type = next((word for word in operation_types if word.upper() in [part.upper() for part in command_parts]), "PREDICTION")
        dataset_train_name = command_parts[[part.upper() for part in command_parts].index("FROM") + 1].split(';')[0]
        features = command_parts[[part.upper() for part in command_parts].index("FEATURES") + 1].split(',')
        algorithm_name = (
            command_parts[[part.upper() for part in command_parts].index("ALGORITHM") + 1]
            if "ALGORITHM" in [part.upper() for part in command_parts]
            else None
        )
    except:
        pass    

    global model, accuracy, label_name, response
    response = {'text': [], 'graph': '', 'table': ''}

    try:
        connection_string = os.getenv("POSTGES_URL")
        query = f'SELECT * FROM "{dataset_train_name}"'
        conn = create_engine(connection_string)
        df = pd.read_sql_query(query, conn)
        X = df[features]
    except sqlalchemy.exc.ProgrammingError as e:
        error_message = str(e.orig)
        response['text'].append( f"Error Occurred! {error_message}")
        return response

    y = None
    model = None 
    accuracy = None

    if operation_type.upper() != "CLUSTERING":
        if operation_type.upper() == "CLASSIFICATION":
            target = command_parts[[part.upper() for part in command_parts].index("CLASSIFICATION") + 1]
        elif operation_type.upper() == "PREDICTION":
            target = command_parts[[part.upper() for part in command_parts].index("PREDICTION") + 1]
        y = df[target]

    if "OVER" in [part.upper() for part in command_parts]:
        df = load_over_df(command_parts[[part.upper() for part in command_parts].index('OVER') + 1])
        if "USING MODEL" in [part.upper() for part in command_parts]:
            load_saved_model(command_parts[[part.upper() for part in command_parts].index("MODEL") + 1] if "MODEL" in [part.upper() for part in command_parts] else "iris_knn")
        else:
            test_s = float(command_parts[[part.upper() for part in command_parts].index("TEST") + 2]) if "TEST" in [part.upper() for part in command_parts] else 20
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_s/100, random_state=42)
            model = select_algorithm(operation_type, algorithm_name.upper())
            model.fit(X_train, y_train)
        
        X = df[features]
        y_test = df[target]
        y_pred = model.predict(df[features])
        output_file = command_parts[[part.upper() for part in command_parts].index("OVER") + 1] + "_predictions.csv"
        
        if y is not None:
            df["prediction"] = y_pred
        if "LABEL" in [part.upper() for part in command_parts]:
            label = command_parts[[part.upper() for part in command_parts].index("LABEL") + 1]
            df.insert(0, label, range(1, len(df) + 1))
        
        response['table'] = df.to_dict(orient="records")
        url = os.path.join(os.path.dirname(__file__), f"../table/table_.csv")
        df.to_csv(url, index=False)
        
        if operation_type.upper() == "CLASSIFICATION" and y_test is not None:
            accuracy = accuracy_score(y_test, y_pred) * 100
            response['text'] += f"Accuracy is {accuracy}. "
        elif operation_type.upper() == "PREDICTION" and y_test is not None:
            accuracy = r2_score(y_test, y_pred) * 100
            response['text'] += f"R2 score is {accuracy}. "
        
        print(f"Predictions saved to {output_file}")

    elif "USING MODEL" in [part.upper() for part in command_parts] and y is not None:
        model_name = command_parts[[part.upper() for part in command_parts].index("MODEL") + 1] if "MODEL" in [part.upper() for part in command_parts] else "iris_knn"
        test_s = float(command_parts[[part.upper() for part in command_parts].index("TEST") + 2]) if "TEST" in [part.upper() for part in command_parts] else 20
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_s/100, random_state=42)
        
        url = os.path.join(os.path.dirname(__file__), f"../model/{model_name}.pkl")
        try:
            with open(url, 'rb') as file:
                model = pickle.load(file)
        except:
            response["text"] = f"Model [{model_name}] Not found."
            return response
        
        y_pred = model.predict(X_test)
        y_pred_df = pd.DataFrame(y_pred, index=y_test.index, columns=["Predicted"])
        df_combined = pd.concat([X_test, y_test, y_pred_df], axis=1)
        
        if "LABEL" in [part.upper() for part in command_parts]:
            label = command_parts[[part.upper() for part in command_parts].index("LABEL") + 1]
            df_combined.insert(0, label, range(1, len(df_combined) + 1))
        
        df_combined = pd.DataFrame(df_combined)
        response['table'] = df_combined.to_dict(orient="records")
        url = os.path.join(os.path.dirname(__file__), f"../table/table_.csv")
        df_combined.to_csv(url, index=False)
        
        ex_ac = command_parts[[part.upper() for part in command_parts].index("ACCURACY") + 1] if "ACCURACY" in [part.upper() for part in command_parts] else 0
        
        if operation_type.upper() == "CLASSIFICATION" and y_test is not None:
            accuracy = accuracy_score(y_test, y_pred) * 100
            if accuracy < float(ex_ac):
                response['text'] = f"Accuracy is less than {accuracy}. "
                return response
            response['text'] = f"Accuracy is {accuracy}. "
        elif operation_type.upper() == "PREDICTION" and y_test is not None:
            accuracy = r2_score(y_test, y_pred) * 100
            if accuracy < float(ex_ac):
                response['text'] = f"R-squared score is less than {accuracy}. "
                return response
            response['text'] = f"R-squared score is {accuracy}. "
    
    elif y is not None and operation_type.upper() != "CLUSTERING":
        test_s = float(command_parts[[part.upper() for part in command_parts].index("TEST") + 2]) if "TEST" in [part.upper() for part in command_parts] else 20
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_s/100, random_state=42)
        
        if not algorithm_name:
            algorithm_name = 'AUTO_ML'
        
        model = select_algorithm(operation_type, algorithm_name.upper())
        model.fit(X_train, y_train)
        
        if "TPOT" in str(model): 
            response['text'].append(  f"{json.dumps(str(model.fitted_pipeline_.steps[0]))}. ")
        
        y_pred = model.predict(X_test)
        y_pred_df = pd.DataFrame(y_pred, index=y_test.index, columns=["Predicted"])
        df_combined = pd.concat([X_test, y_test, y_pred_df], axis=1)
        
        if "LABEL" in [part.upper() for part in command_parts]:
            label = command_parts[[part.upper() for part in command_parts].index("LABEL") + 1]
            df_combined.insert(0, label, range(1, len(df_combined) + 1))
        
        response['table'] = df_combined.to_dict(orient="records")
        url = os.path.join(os.path.dirname(__file__), f"../table/table_.csv")
        df_combined.to_csv(url, index=False)
        
        if operation_type.upper() == "CLASSIFICATION" and y_test is not None:
            ex_ac = command_parts[[part.upper() for part in command_parts].index("ACCURACY") + 1] if "ACCURACY" in [part.upper() for part in command_parts] else 0
            accuracy = accuracy_score(y_test, y_pred) * 100
            if accuracy < float(ex_ac):
                response['text'].append( f"Accuracy is less than {accuracy}. ")
                if algorithm_name != "AUTO_ML":
                    response['text'].append(  f" Trying another model ")
                    model = select_algorithm(operation_type, "AUTO_ML")
                    model.fit(X_train, y_train)
                    response['text'].append(  f"{json.dumps(str(model.fitted_pipeline_.steps[0]))} . ")
                    y_pred = model.predict(X_test)
                    y_pred_df = pd.DataFrame(y_pred, index=y_test.index, columns=["Predicted"])
                    df_combined = pd.concat([X_test, y_test, y_pred_df], axis=1)
                    response['table'] = df_combined.to_dict(orient="records")
            else:
                response['text'].append(  f"Accuracy is {accuracy}. ")
        elif operation_type.upper() == "PREDICTION" and y_test is not None:
            ex_ac = command_parts[[part.upper() for part in command_parts].index("ACCURACY") + 1] if "ACCURACY" in [part.upper() for part in command_parts] else command_parts[[part.upper() for part in command_parts].index("R-SQUARED") + 1] if "R-SQUARED" in [part.upper() for part in command_parts] else 0
            accuracy = r2_score(y_test, y_pred) * 100
            if accuracy < float(ex_ac):
                response['text'].append( f"R-squared score is less than {accuracy}. ")
                if algorithm_name != "AUTO_ML":
                    response['text'].append(  f"Trying another model... ")
                    model = select_algorithm(operation_type, "AUTO_ML")
                    model.fit(X_train, y_train)
                    response['text'].append( f"{json.dumps(str(model.fitted_pipeline_.steps[0]))} . ")
                    y_pred = model.predict(X_test)
                    y_pred_df = pd.DataFrame(y_pred, index=y_test.index, columns=["Predicted"])
                    df_combined = pd.concat([X_test, y_test, y_pred_df], axis=1)
                    response['table'] = df_combined.to_dict(orient="records")
            else:
                response['text'].append( f"R-squared score is {accuracy}. ")
    
    else:
        n_cluster = command_parts[[part.upper() for part in command_parts].index("CLUSTER") + 2] if "CLUSTER" in [part.upper() for part in command_parts] else 3
        if algorithm_name == 'default':
            algorithm_name = KMeans
        model = select_algorithm(operation_type, algorithm_name.upper(), n_clusters=n_cluster)
        X = pd.DataFrame(X.select_dtypes(include=[np.number]))
        model.fit(X)
        y_pred = model.labels_
        df = df[features]
        df['Class'] = y_pred.tolist()
        df = pd.DataFrame(df)
        response['table'] = df.to_dict(orient='records')
        url = os.path.join(os.path.dirname(__file__), f"../table/table_.csv")
        df.to_csv(url, index=False)

    if "DISPLAY" in [part.upper() for part in command_parts]:
        response['graph'] = display_results(operation_type, y_test if y is not None else None, y_pred, model, features, df)
        if response['graph']:
            print("Graph generated")
    
    return response
