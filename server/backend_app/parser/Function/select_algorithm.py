
import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN, AgglomerativeClustering, KMeans
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from sklearn.svm import SVR, SVC


from ..Function.display_result import display_results
from ..Function import *
from torch.utils.data import DataLoader, TensorDataset
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense



def select_algorithm(operation_type, algorithm_name, **kwargs):
    
    print(algorithm_name, operation_type)
    # Scikit-learn models
    prediction_algorithms = {
        "LR": LinearRegression(),
        "RF": RandomForestRegressor(),
        "KNN": KNeighborsRegressor(),
        "SVR": SVR(),
        "GBR": GradientBoostingRegressor(),
    }
    classification_algorithms = {
        "LOG": LogisticRegression(),
        "RFC": RandomForestClassifier(),
        "KNN": KNeighborsClassifier(),
        "SVC": SVC(),
        "GBC": GradientBoostingClassifier(),
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
