import os
import pickle
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score, r2_score, silhouette_score
from sklearn.cluster import KMeans
import json


def flaml(X_train, X_test, y_train, y_test, target, operation_type, features=None, n_clusters=3):
    """
    FLAML (Fast and Lightweight AutoML) implementation
    """
    print("flaml started")
    try:
        from flaml import AutoML
        
        if operation_type.lower() == "clustering":
            # FLAML doesn't support clustering directly, so we'll use KMeans and optimize hyperparameters
            print("FLAML doesn't support clustering directly. Using KMeans with optimized parameters.")
            k = n_clusters if n_clusters else 3
            if hasattr(X_train, 'shape'):
                k = min(k, X_train.shape[0])
            
            # Use a simple KMeans for clustering
            model = KMeans(n_clusters=k, random_state=42, n_init=10)
            cluster_labels = model.fit_predict(X_train)
            
            # Silhouette score as main metric
            if len(set(cluster_labels)) > 1:
                score = silhouette_score(X_train, cluster_labels)
            else:
                score = 0.0
            
            return score, list(cluster_labels), model
            
        else:
            # Initialize FLAML AutoML
            automl = AutoML()
            
            # Set task type and time budget
            if operation_type.lower() == "classification":
                task = "classification"
                metric = "accuracy"
            elif operation_type.lower() == "prediction":
                task = "regression" 
                metric = "r2"
            else:
                raise ValueError(f"Unsupported operation type: {operation_type}")
            
            # Configure FLAML settings
            settings = {
                "time_budget": 120,  # 2 minutes
                "metric": metric,
                "task": task,
                "log_file_name": "flaml.log",
                "seed": 42,
                "verbose": 0,
                "ensemble": True,
                "eval_method": "cv",
                "split_ratio": 0.2,
                "n_jobs": -1
            }
            
            # Fit the model
            automl.fit(X_train, y_train, **settings)
            
            # Make predictions
            y_pred = automl.predict(X_test)
            
            # Calculate score
            if operation_type.lower() == "classification":
                score = accuracy_score(y_test, y_pred)
            elif operation_type.lower() == "prediction":
                score = r2_score(y_test, y_pred)
            
            print(f"FLAML best model: {automl.best_estimator}")
            print(f"FLAML best config: {automl.best_config}")
            print(f"FLAML best score: {score}")
            
            return score, list(y_pred), automl
            
    except Exception as e:
        print(f"flaml failed: {e}")
        return None, None, None
    finally:
        print("flaml ended")
