from matplotlib import pyplot as plt, rcParams
import base64
import io
import os
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import uuid
from django.conf import settings
from sklearn.metrics import  confusion_matrix


matplotlib.use('Agg')


def display_results(operation_type, y_test=None, y_pred=None, model=None, features=None, df=None):
    if operation_type.upper() == "PREDICTION":
        plt.figure(figsize=(10, 6))
        plt.scatter(y_test, y_pred)
        plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()])
        plt.xlabel('Measured')
        plt.ylabel('Predicted')
        plt.title('Actual vs Predicted Values')
    elif operation_type.upper() == "CLASSIFICATION":
        cm = confusion_matrix(y_test, y_pred)
        sns.heatmap(cm, cmap='Blues')
        plt.xlabel('Predicted')
        plt.ylabel('Actual')
        plt.title('Confusion Matrix')
    elif operation_type.upper() == "CLUSTERING":
        if len(features) >= 2:
            plt.figure(figsize=(10, 6))
            sns.scatterplot(data=pd.DataFrame(df), x=features[0], y=features[1], hue='Class', palette='viridis')
            
            if hasattr(model, 'cluster_centers_'):
                plt.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1], 
                          c='red', s=100, marker='x', label='Centroids', linewidths=3)
            
            plt.title('Clustering Results')
            plt.legend(title="Cluster")
        else:
            plt.figure(figsize=(10, 6))
            plt.text(0.5, 0.5, 'Need at least 2 features for clustering visualization', 
                    ha='center', va='center', transform=plt.gca().transAxes)
            plt.title('Clustering Results')

    formats = ["png", "svg", "jpg"]
    response = {}

    for fmt in formats:
        file_name = f"graph_{uuid.uuid4()}.{fmt}"
        file_path = os.path.join(settings.MEDIA_ROOT, file_name)
        plt.savefig(file_path, format=fmt)
        response[f'graph_{fmt}'] = os.path.join(settings.MEDIA_URL, file_name)
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = None #base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return plot_data,response, os.path.join(settings.MEDIA_URL, file_name)