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
def select_algorithm(operation_type, algorithm_name, **kwargs):
    if algorithm_name == 'AUTO_ML':
        if operation_type.upper() == "PREDICTION":
            tpot_regressor = TPOTRegressor(generations=2, population_size=5, verbosity=2)
            print("in tpot",tpot_regressor)
            return tpot_regressor
        elif operation_type.upper() == "CLASSIFICATION":
            tpot_classifier = TPOTClassifier(generations=1, population_size=1, verbosity=1)
            return tpot_classifier

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