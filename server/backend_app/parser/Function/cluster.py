from altair import Orient
from numpy import record
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import base64
import io
import json

def cluster(currentDB,conn, n_cluster):
    query = f"SELECT * FROM {currentDB}"
    df = pd.read_sql_query(query, conn)
    # Perform clustering
    X = df.values  # Assuming all columns are features
    kmeans = KMeans(n_clusters=int(n_cluster))
    kmeans.fit(X)
    labels = kmeans.labels_

    plt.figure(figsize=(8, 6))
    plt.scatter(X[:, 0], X[:, 1], c=labels, cmap='viridis')
    plt.title('Clusters')
    plt.xlabel('Feature 1')
    plt.ylabel('Feature 2')
    plt.grid(True)
    # plt.show()
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # labels_list = labels.tolist()

    plt.close()
    df['Class'] = labels.tolist()
    df=pd.DataFrame(df)
    df=df.to_dict(orient='records')
    response = {
        # 'table': df,
        'graph': plot_data,
        'text' : f"Cluster on{currentDB}"
    }
    return response
