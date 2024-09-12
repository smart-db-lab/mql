import base64
import io
from matplotlib import pyplot as plt
import numpy as np
import pandas as pd
import os
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN

from ..Function.select_algorithm import select_algorithm

def Clustering(command_parts,operation_type,algorithm_name,features,response,X):
    n_cluster = command_parts[[part.upper() for part in command_parts].index("CLUSTER") + 2] if "CLUSTER" in [part.upper() for part in command_parts] else 3
    if algorithm_name == 'default':
        algorithm_name = KMeans
    model = select_algorithm(operation_type, algorithm_name.upper(), n_clusters=n_cluster)
    X = pd.DataFrame(X.select_dtypes(include=[np.number]))
    model.fit(X)
    labels = model.labels_
    cluster_df = X[features]
    cluster_df['Class'] = labels.tolist()
    cluster_df = pd.DataFrame(cluster_df)
    response['table'] = cluster_df.to_dict(orient='records')
    url = os.path.join(os.path.dirname(__file__), f"../table/table_.csv")
    cluster_df.to_csv(url, index=False)

    return response,model,labels,cluster_df
