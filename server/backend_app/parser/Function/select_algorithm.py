import io
import json
import sqlite3
import uuid
import os
import dill
import pickle
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.calibration import LabelEncoder
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
import sqlalchemy
import torch
import torch.nn as nn
import torch.optim as optim
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.metrics import accuracy_score, confusion_matrix, r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from tpot import TPOTRegressor, TPOTClassifier
from sqlalchemy import create_engine

from ..Function.display_result import display_results
from ..Function import *
from torch.utils.data import DataLoader, TensorDataset
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense

from pycaret.regression import *
from pycaret.classification import *
from pycaret.clustering import *
import h2o
from h2o.automl import H2OAutoML




def select_algorithm(operation_type, algorithm_name, **kwargs):
    if algorithm_name == 'tpot':
        if operation_type.upper() == "PREDICTION":
            from tpot import TPOTRegressor
            return TPOTRegressor(generations=2, population_size=5, verbosity=2)
        elif operation_type.upper() == "CLASSIFICATION":
            from tpot import TPOTClassifier
            return TPOTClassifier(generations=1, population_size=1, verbosity=1)

    elif algorithm_name == 'pycaret':
        if operation_type.upper() == "PREDICTION":
            if 'data' in kwargs and 'target' in kwargs:
                exp = RegressionExperiment()
                exp.setup(data=kwargs['data'], target=kwargs['target'], session_id=123,)
                return exp
            else:
                raise ValueError("For PyCaret prediction, 'data' and 'target' must be provided in kwargs.")

        elif operation_type.upper() == "CLASSIFICATION":
            if 'data' in kwargs and 'target' in kwargs:
                if kwargs['target'] not in kwargs['data'].columns:
                    raise ValueError(f"Target column '{kwargs['target']}' not found in the provided data.")
                exp = ClassificationExperiment()
                exp.setup(data=kwargs['data'], target=kwargs['target'], session_id=123)
                return exp
            else:
                raise ValueError("For PyCaret classification, 'data' and 'target' must be provided in kwargs.")

        elif operation_type.upper() == "CLUSTERING":
            if 'data' in kwargs:
                exp = ClusteringExperiment()
                exp.setup(data=kwargs['data'], session_id=123)
                return exp
            else:
                raise ValueError("For PyCaret clustering, 'data' must be provided in kwargs.")
    elif algorithm_name == 'h2o':
        h2o.init()
        if operation_type.upper() == "PREDICTION":
            aml = H2OAutoML(max_models=20, seed=1)
            print("H2O AutoML for Prediction initialized")
            return aml
        elif operation_type.upper() == "CLASSIFICATION":
            aml = H2OAutoML(max_models=20, seed=1)
            print("H2O AutoML for Classification initialized")
            return aml
        elif operation_type.upper() == "CLUSTERING":
            print("H2O AutoML does not directly support clustering")
            return None

        
    print(algorithm_name, operation_type)
    # Scikit-learn models
    prediction_algorithms = {
        "LR": LinearRegression(),
        "RF": RandomForestRegressor(),
        "KNN": KNeighborsRegressor(),
    }
    classification_algorithms = {
        "LOG": LogisticRegression(),
        "RFC": RandomForestClassifier(),
        "KNN": KNeighborsClassifier(),
    }
    clustering_algorithms = {
        "KMEANS": KMeans(n_clusters=(int(kwargs.get('n_clusters')) if kwargs.get('n_clusters') else 3)),
        "AGGLOMERATIVE": AgglomerativeClustering(),
        "DBSCAN": DBSCAN(),
    }
    algorithms = {
        "PREDICTION": prediction_algorithms,
        "CLASSIFICATION": classification_algorithms,
        "CLUSTERING": clustering_algorithms
    }
    selected_algorithms = algorithms.get(operation_type.upper(), prediction_algorithms)
    return selected_algorithms.get(algorithm_name.upper())
