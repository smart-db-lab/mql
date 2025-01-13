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
from ..Function.select_algorithm import select_algorithm


from sklearn.metrics import accuracy_score, r2_score
from torch.utils.data import DataLoader, TensorDataset
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense
matplotlib.use('Agg')

def train_and_evaluate_auto_ml(model, X_train, X_test, y_train, y_test,operation_type):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    # if hasattr(model, 'score'):
    if operation_type.upper()=="CLASSIFICATION":
        print("in score ")
        score = accuracy_score(y_test, y_pred)
        print(score)
        try:
            print(".score", model.score(X_test, y_test))
            score= model.score(X_test, y_test)
        except:
            pass
    else:
        score = r2_score(y_test, y_pred)
    return y_pred, score

def train_and_evaluate_sklearn(model, X_train, X_test, y_train, y_test,operation_type):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    if hasattr(model, 'score'):
        print("in score to")
        score = model.score(X_test, y_test)
    else:
        score = r2_score(y_test, y_pred)
    return y_pred, score

class SimpleNN(nn.Module):
    def __init__(self, input_dim, output_dim, classification=False):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 128)
        self.fc2 = nn.Linear(128, 64)
        self.fc3 = nn.Linear(64, output_dim)
        self.classification = classification

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        if self.classification:
            x = torch.softmax(x, dim=1)  # Use softmax for classification
        return x

def train_and_evaluate_torch(model, X_train, X_test, y_train, y_test, epochs=3, learning_rate=0.001, classification=False):
    # Select appropriate criterion
    criterion = nn.CrossEntropyLoss() if classification else nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # Convert data to tensors
    X_train = pd.DataFrame(X_train)
    X_test = pd.DataFrame(X_test)
    X_train_tensor = torch.tensor(X_train.values, dtype=torch.float32)
    y_train_tensor = torch.tensor(y_train.values, dtype=torch.long if classification else torch.float32)
    X_test_tensor = torch.tensor(X_test.values, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test.values, dtype=torch.long if classification else torch.float32)
    
    # Debugging prints
    # print(f"Shapes: X_train_tensor: {X_train_tensor.shape}, y_train_tensor: {y_train_tensor.shape}")
    # print(f"Shapes: X_test_tensor: {X_test_tensor.shape}, y_test_tensor: {y_test_tensor.shape}")

    # Create DataLoader
    train_dataset = TensorDataset(X_train_tensor, y_train_tensor)
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)

    # Training loop
    for epoch in range(epochs):
        model.train()
        for X_batch, y_batch in train_loader:
            optimizer.zero_grad()
            outputs = model(X_batch)
            # Debugging prints
            # print(f"Epoch {epoch+1}, Batch shapes - X_batch: {X_batch.shape}, y_batch: {y_batch.shape}, outputs: {outputs.shape}")

            if classification:
                loss = criterion(outputs, y_batch)
            else:
                loss = criterion(outputs.squeeze(), y_batch)
            loss.backward()
            optimizer.step()

    # Evaluate the model
    model.eval()
    with torch.no_grad():
        y_pred_tensor = model(X_test_tensor)
        # Debugging prints
        # print(f"Evaluation shapes - X_test_tensor: {X_test_tensor.shape}, y_test_tensor: {y_test_tensor.shape}, y_pred_tensor: {y_pred_tensor.shape}")

        if classification:
            y_pred = torch.argmax(y_pred_tensor, dim=1).numpy()
        else:
            y_pred = y_pred_tensor.numpy().flatten()

        # Compute R² score or accuracy
        if classification:
            accuracy = accuracy_score(y_test, y_pred)
            print(f"Accuracy: {accuracy}")
            return y_pred, accuracy
        else:
            r2 = r2_score(y_test, y_pred)
            print(f"R² Score: {r2}")
            return y_pred, r2


def train_and_evaluate_tf(model, X_train, X_test, y_train, y_test, epochs=3, classification=False):
    # Fit the model
    model.fit(X_train, y_train, epochs=epochs, verbose=0)
    
    # Predict on the test set
    y_pred = model.predict(X_test)
    
    # Ensure y_test is flattened if it's a single-column 2D array
    if y_test.ndim > 1 and y_test.shape[1] == 1:
        y_test = y_test.flatten()

    if classification:
        # For classification, ensure predictions are argmaxed
        y_pred = np.argmax(y_pred, axis=1)
        # Ensure y_test and y_pred have the same shape
        assert y_test.shape == y_pred.shape, f"Shapes of y_test {y_test.shape} and y_pred {y_pred.shape} do not match."
        # Calculate accuracy
        accuracy = accuracy_score(y_test, y_pred)
        return y_pred, accuracy
    else:
        # For regression, flatten the predictions
        y_pred = y_pred.flatten()
        # Ensure y_test and y_pred have the same shape
        assert y_test.shape == y_pred.shape, f"Shapes of y_test {y_test.shape} and y_pred {y_pred.shape} do not match."
        # Calculate R^2 score
        score = r2_score(y_test, y_pred)
        return y_pred, score

def build_tf_model(input_dim, output_dim, classification):
    model = Sequential([
        Dense(64, activation='relu', input_dim=input_dim),
        Dense(64, activation='relu'),
        Dense(output_dim, activation='softmax' if classification else None)
    ])
    loss = 'sparse_categorical_crossentropy' if classification else 'mse'
    model.compile(optimizer='adam', loss=loss, metrics=['accuracy'] if classification else ['mae'])
    return model

def load_over_df(df_name):
    url = os.path.join(os.path.dirname(__file__), f"../../data/files/{df_name}.csv")
    return pd.read_csv(url)

def load_saved_model(model_name,response):
    url = os.path.join(os.path.dirname(__file__), f"../model/{model_name}.pkl")
    try:
        with open(url, 'rb') as file:
            model = pickle.load(file)  
            print(f"Model loaded successfully from {url}")
            return model,response
    except:
        response["text"] = f"Model: [{model_name}] Not found."
        return None,response