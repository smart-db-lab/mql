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
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, r2_score, mean_squared_error

import sqlalchemy
from sympy import plot

from ..Function.Clustering import Clustering
from ..Function.display_result import display_results
from ..Function.select_algorithm import select_algorithm
from ..classes.load_data import *
from ..classes.dl_algo import *
from sqlalchemy import create_engine
matplotlib.use('Agg')

def handle_over(command_parts,features,target,y,operation_type,algorithm_name,response):
    df = load_over_df(command_parts[[part.upper() for part in command_parts].index('OVER') + 1])
    if "USING MODEL" in [part.upper() for part in command_parts]:
        model,response=load_saved_model(command_parts[[part.upper() for part in command_parts].index("MODEL") + 1] if "MODEL" in [part.upper() for part in command_parts] else "iris_knn",response)
        if model is None :
            return response
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
    return response

def temp_generate(command):  
    command_upper=command.upper()
    command_parts = [part for part in command.split(" ") if part.strip()]
    try:
        operation_types = ["PREDICTION", "CLASSIFICATION", "CLUSTERING"]
        operation_type = next((word for word in operation_types if word.upper() in [part.upper() for part in command_parts]), "PREDICTION")
        dataset_train_name = command_parts[[part.upper() for part in command_parts].index("FROM") + 1].split(';')[0]
        features = command_parts[[part.upper() for part in command_parts].index("FEATURES") + 1].split(',')
        algorithm_name = (
            command_parts[[part.upper() for part in command_parts].index("ALGORITHM") + 1]
            if "ALGORITHM" in [part.upper() for part in command_parts]
            else ""
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
    except sqlalchemy.exc.ProgrammingError as e:
        error_message = str(e.orig)
        response['text'] = f"Error Occurred! {error_message}"
        return response
    feature_part=command_parts[[part.upper() for part in command_parts].index("FEATURES") + 1].strip()
    if "OVER" in [part.upper() for part in command_parts]:
        Over_df = load_over_df(command_parts[[part.upper() for part in command_parts].index('OVER') + 1].split(';')[0])
        features= Over_df.columns.tolist() if '*' in feature_part else feature_part.split(',') 
    else: features= df.columns.tolist() if '*' in feature_part else feature_part.split(',') 
    y = None
    model = None 
    accuracy = None
    label_encoder = LabelEncoder()
    
    if operation_type.upper() != "CLUSTERING":
        if operation_type.upper() == "CLASSIFICATION":
            target = command_parts[[part.upper() for part in command_parts].index("CLASSIFICATION") + 1]
        elif operation_type.upper() == "PREDICTION":
            target = command_parts[[part.upper() for part in command_parts].index("PREDICTION") + 1]
            if "OVER" in  [part.upper() for part in command_parts] and not Over_df.select_dtypes(include='object').columns.empty :
                try: features.remove(Over_df.select_dtypes(include='object').columns)
                except: pass
            if not (df.select_dtypes(include='object').columns.empty):
                try:   features.remove(df.select_dtypes(include='object').columns)
                except: pass

        y = df[target]
        if target in features:
            features.remove(target)
        if operation_type.upper() == "CLASSIFICATION":
            y_encoded = label_encoder.fit_transform(y)
            y=pd.Series(y_encoded, name=target)

    X = df[features]
    
    if operation_type.upper() == "CLUSTERING":
        response,model,y_pred_df,df = Clustering(command_parts,operation_type,algorithm_name,features,response,X)
        # return response
    elif y is not None and operation_type.upper() != "CLUSTERING":
        test_s = float(command_parts[[part.upper() for part in command_parts].index("TEST") + 2]) if "TEST" in [part.upper() for part in command_parts] else 20
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_s/100, random_state=42)
        
        # # Scale the data
        # scaler = StandardScaler()
        # X_train = scaler.fit_transform(X_train)
        # X_test = scaler.transform(X_test)

        models = {
            'sklearn': select_algorithm(operation_type, algorithm_name),
            'pytorch': SimpleNN(X_train.shape[1], len(np.unique(y_train)) if operation_type.upper()=="CLASSIFICATION" else 1, classification=operation_type.upper()=="CLASSIFICATION"),
            'tensorflow': build_tf_model(X_train.shape[1], len(np.unique(y_train)) if operation_type.upper()=="CLASSIFICATION" else 1, classification=operation_type.upper()=="CLASSIFICATION"),
            'Auto-ML': select_algorithm(operation_type.upper(),"AUTO_ML"),
        }
        print(models['Auto-ML'])
        results = {}
        y_pred_Frame={}
        if "OVER" in [part.upper() for part in command_parts]:
            X_test = Over_df[features]
            y_test = Over_df[target]
        
         #auto ml
        y_pred_Frame['Auto-ML'],score=train_and_evaluate_auto_ml(models['Auto-ML'],X_train, X_test, y_train, y_test,operation_type)
        results['Auto-ML']= score
        print("auto",results['Auto-ML'])
        print((models['Auto-ML'].fitted_pipeline_.steps[0][1]))
        auto_algo=f"{json.dumps(str(models['Auto-ML'].fitted_pipeline_.steps[0][1]).split('(')[0])}"
        print(auto_algo)
        # Sklearn
        if "USING MODEL" in command_upper:
            model,response= load_saved_model(command_parts[[part.upper() for part in command_parts].index("MODEL") + 1] if "MODEL" in [part.upper() for part in command_parts] else "iris_knn",response)
            if model is None :
                return response
            model.fit(X_train, y_train)
            y_pred_Frame["sklearn"] = model.predict(X_test)
            if operation_type.upper()=="PREDICTION":
                score_sklearn = r2_score(y_test, y_pred_Frame["sklearn"])
            else:
                score_sklearn = accuracy_score(y_test, y_pred_Frame["sklearn"])
            results['sklearn'] = score_sklearn
        else:
            y_pred_Frame["sklearn"], score_sklearn = train_and_evaluate_sklearn(models['sklearn'], X_train, X_test, y_train, y_test,operation_type)
        results['sklearn'] = score_sklearn
        print("sk",algorithm_name,score_sklearn)
        
        # Scale the data
        # scaler = StandardScaler()
        # X_train = scaler.fit_transform(X_train)
        # X_test = scaler.transform(X_test)

        # TensorFlow
        y_pred_Frame["pytorch"], score_torch = train_and_evaluate_torch(models['pytorch'], X_train, X_test, y_train, y_test, epochs=1, classification=operation_type.upper()=="CLASSIFICATION")
        results['tensorflow'] = score_torch
        
        # PyTorch
        y_pred_Frame["tensorflow"], score_tf = train_and_evaluate_tf(models['tensorflow'], X_train, X_test, y_train, y_test, epochs=1, classification=operation_type.upper()=="CLASSIFICATION")
        results['pytorch'] = score_tf

        results= dict(sorted(results.items(), key=lambda item: item[1], reverse=True))
        response["text"].append(results)
        print(results)
        
        best_framework = max(results, key=results.get)
        if best_framework=="Auto-ML":
            algorithm_name=auto_algo
        best_score = results[best_framework]
        # df=pd.DataFrame(df)
        X_test=pd.DataFrame(X_test)

        y_pred_df = pd.DataFrame(y_pred_Frame[best_framework] , index=y_test.index, columns=["Predicted"])

        df = pd.concat([X_test, y_test, y_pred_df], axis=1)
        
        if "LABEL" in [part.upper() for part in command_parts]:
            label = command_parts[[part.upper() for part in command_parts].index("LABEL") + 1]
            df.insert(0, label, range(1, len(df) + 1))
        response['table'] = df.to_dict(orient="records")
        url = os.path.join(os.path.dirname(__file__), f"../table/table_.csv")
        df.to_csv(url, index=False)
        
        response['text'].append(str(f"Best Algorithm: {algorithm_name} By {best_framework} with score: {best_score}"))

    if "DISPLAY" in [part.upper() for part in command_parts]:
        response['graph'] = display_results(operation_type, y_test if y is not None else None, y_pred_df, model, features, df)
        if response['graph']:
            print("Graph generated")
    return response
