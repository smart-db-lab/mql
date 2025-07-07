import os
import pandas as pd
import uuid
import numpy as np
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from django.conf import settings

from ..Function.display_result import display_results
from ..Function.select_algorithm import select_algorithm
from ..classes.load_data import load_over_df
from ..classes.dl_algo import train_and_evaluate_sklearn, load_saved_model, load_over_df

from .utils import save_model_pickle, get_connection, get_arg, is_flag_present, parse_features, parse_command_parts, get_operation_type

def clustering_generate(command, user=None):
    """
    Comprehensive clustering operation similar to Temp_Generate.py
    Supports multiple autoML libraries, creates cluster graphs, tables with class columns
    """
    command_parts = command.strip().split()
    response = {'text': [], 'graph': '', 'table': '', 'query': command}
    operation_type = "CLUSTERING"  # This function is specifically for clustering
    
    # Get dataset name
    dataset_name = get_arg(command_parts, "FROM", "").split(';')[0]
    if not dataset_name:
        response['text'].append("Error: Dataset name not found. Use 'FROM dataset_name'")
        return response

    # Load dataset
    try:
        conn = get_connection()
        df = pd.read_sql_query(f'SELECT * FROM "{dataset_name}"', conn)
    except Exception as e:
        response['text'].append(f"Error loading dataset: {e}")
        return response

    # Parse features
    feature_str = get_arg(command_parts, "FEATURES", "")
    Over_df = load_over_df(get_arg(command_parts, "OVER", "").split(';')[0]) if is_flag_present(command_parts, "OVER") else None
    features = parse_features(Over_df if Over_df is not None else df, feature_str)
    
    # Get algorithm and number of clusters
    algorithm_name = get_arg(command_parts, "ALGORITHM", "KMEANS")
    n_clusters = int(get_arg(command_parts, "CLUSTER",offset=2, default=""))
    
    # Prepare data
    X = df[features].select_dtypes(include=[np.number])
    if X.empty:
        response['text'].append("Error: No numeric features found for clustering")
        return response
    
    # Initialize models dictionary
    models = {
        'sklearn': select_algorithm(operation_type, algorithm_name, n_clusters=n_clusters),
        'pycaret': None,
        'h2o': None,
        'tpot': None,
        'autosklearn2': None
    }
    
    results = {}
    y_preds = {}
    cluster_dfs = {}
    
    # === Start sklearn clustering ===
    try:
        model = models['sklearn']
        if model is not None:
            model.fit(X)
            labels = model.labels_
            y_preds['sklearn'] = labels
            # Calculate clustering metrics
            if len(np.unique(labels)) > 1:
                try:
                    silhouette = silhouette_score(X, labels)
                    results['sklearn'] = silhouette
                except Exception as e:
                    print(f"Error calculating sklearn metrics: {e}")
                    results['sklearn'] = 0.0
            else:
                results['sklearn'] = 0.0
            cluster_df = X.copy()
            cluster_df['Class'] = labels
            cluster_dfs['sklearn'] = cluster_df
            response['text'].append(f"Sklearn {algorithm_name} clustering completed with {len(np.unique(labels))} clusters")
    except Exception as e:
        print(f"Sklearn clustering failed: {e}")
        results['sklearn'] = None

    # === Start PyCaret clustering ===
    try:
        from ..auto_ml.pycaret import pycaret
        score, labels, model = pycaret(X, None, None, None, None, operation_type)
        if score is not None and labels is not None:
            models['pycaret'] = model
            y_preds['pycaret'] = labels
            results['pycaret'] = score
            cluster_df = X.copy()
            cluster_df['Class'] = labels
            cluster_dfs['pycaret'] = cluster_df
            response['text'].append(f"PyCaret clustering completed with {len(np.unique(labels))} clusters")
        else:
            response['text'].append("PyCaret clustering not implemented for this operation")
    except Exception as e:
        print(f"PyCaret clustering failed: {e}")
        results['pycaret'] = None

    # === Start H2O clustering ===
    try:
        from ..auto_ml.h2o import h2o
        score, labels, model = h2o(X, None, None, None, None, operation_type, features,n_clusters)
        if score is not None and labels is not None:
            models['h2o'] = model
            y_preds['h2o'] = labels
            results['h2o'] = score
            cluster_df = X.copy()
            cluster_df['Class'] = labels
            cluster_dfs['h2o'] = cluster_df
            response['text'].append(f"H2O clustering completed with {len(np.unique(labels))} clusters")
        else:
            response['text'].append("H2O clustering not implemented for this operation")
    except Exception as e:
        print(f"H2O clustering failed: {e}")
        results['h2o'] = None

    # === Start TPOT clustering ===
    try:
        from ..auto_ml.tpot import tpot
        score, labels, model = tpot(operation_type, X, None, None, None)
        if score is not None and labels is not None:
            models['tpot'] = model
            y_preds['tpot'] = labels
            results['tpot'] = score
            cluster_df = X.copy()
            cluster_df['Class'] = labels
            cluster_dfs['tpot'] = cluster_df
            response['text'].append(f"TPOT clustering completed with {len(np.unique(labels))} clusters")
        else:
            response['text'].append("TPOT clustering not implemented for this operation")
    except Exception as e:
        print(f"TPOT clustering failed: {e}")
        results['tpot'] = None

    # === Start AutoSklearn2 clustering ===
    try:
        from ..auto_ml.autosklearn2 import autosklearn2
        score, labels, model = autosklearn2(X, None, None, None, operation_type)
        if score is not None and labels is not None:
            models['autosklearn2'] = model
            y_preds['autosklearn2'] = labels
            results['autosklearn2'] = score
            cluster_df = X.copy()
            cluster_df['Class'] = labels
            cluster_dfs['autosklearn2'] = cluster_df
            response['text'].append(f"AutoSklearn2 clustering completed with {len(np.unique(labels))} clusters")
        else:
            response['text'].append("AutoSklearn2 clustering not implemented for this operation")
    except Exception as e:
        print(f"AutoSklearn2 clustering failed: {e}")
        results['autosklearn2'] = None

    # Filter out None results
    valid_results = {k: v for k, v in results.items() if v is not None}
    
    if not valid_results:
        response['text'].append("No clustering models trained successfully.")
        return response
    
    # Find best framework
    best_framework = max(valid_results, key=valid_results.get)
    best_score = valid_results[best_framework]
    best_model = models[best_framework]
    best_labels = y_preds[best_framework]
    best_cluster_df = cluster_dfs[best_framework]
    
    # Create final result dataframe
    df_result = best_cluster_df.copy()
    
    # Add label column if requested
    if is_flag_present(command_parts, "LABEL"):
        label = get_arg(command_parts, "LABEL")
        df_result.insert(0, label, range(1, len(df_result) + 1))
    
    # Save table
    table_dir = os.path.join(settings.MEDIA_ROOT, "tables")
    os.makedirs(table_dir, exist_ok=True)
    
    table_filename = f"cluster_table_{uuid.uuid4().hex}.csv"
    result_path = os.path.join(table_dir, table_filename)
    
    df_result.to_csv(result_path, index=False)
    response['table'] = df_result.replace([float('inf'), float('-inf'), float('nan')], None).to_dict(orient='records')
    
    # Add performance information
    response['text'].append(f"Best Model: {best_framework} with silhouette score {best_score:.4f}")
    response['text'].append(f"Number of clusters: {len(np.unique(best_labels))}")
    
    # Performance Table
    performance_table = []
    for framework, score in results.items():
        if score is not None:
            entry = {
                "Framework": framework, 
                "Score": round(score, 4),
                "Algorithm": str(models[framework]) if models[framework] else "N/A"
            }
            performance_table.append(entry)
        else:
            entry = {
                "Framework": framework, 
                "Score": "N/A",
                "Algorithm": "Not implemented"
            }
            performance_table.append(entry)
    
    performance_table.sort(key=lambda x: (x["Score"] == "N/A", x["Score"]), reverse=True)
    response["performance_table"] = performance_table
    
    # Save best model
    if user:
        model_path = save_model_pickle(
            best_model, user, dataset_name, best_framework, command
        )
        response['text'].append(f"Model saved as: {model_path}")
    
    # Generate graph if requested
    if is_flag_present(command_parts, "DISPLAY"):
        try:
            response['graph'], response['graph_link'], response['graph_path'] = display_results(
                operation_type, None, best_labels, best_model, features, df_result
            )
            # response['text'].append(f"Graph generated: {response['graph_link']}")
        except Exception as e:
            response['text'].append(f"Error generating graph: {e}")
    
    return response
