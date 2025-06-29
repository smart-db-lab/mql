import os
import pickle
import pandas as pd
from sklearn.metrics import accuracy_score, r2_score, silhouette_score


from pycaret.classification import setup as setup_clf, compare_models as compare_classification_models
from pycaret.regression import setup as setup_reg, compare_models as compare_regression_models
from pycaret.clustering import setup as setup_cluster, create_model as create_cluster_model, assign_model as assign_cluster_model
import json
import contextlib

def pycaret(X, y, X_test, y_test, target, operation_type):
    os.environ["PYCARETSILENCE"] = "1"
    os.environ['LIGHTGBM_VERBOSE'] = '0'
    print("pycaret started")
    try:
        if operation_type.lower() == "classification":
            df_full = pd.concat([X, y], axis=1)
            with open(os.devnull, 'w') as devnull, \
                contextlib.redirect_stdout(devnull), \
                contextlib.redirect_stderr(devnull):
                setup_clf(data=df_full, target=target, session_id=42)
                best_pycaret_model = compare_classification_models()
                y_pred = best_pycaret_model.predict(X_test)
                score = accuracy_score(y_test, y_pred)
        elif operation_type.lower() == "prediction":
            df_full = pd.concat([X, y], axis=1)
            with open(os.devnull, 'w') as devnull, \
                contextlib.redirect_stdout(devnull), \
                contextlib.redirect_stderr(devnull):
                setup_reg(data=df_full, target=target, session_id=42)
                best_pycaret_model = compare_regression_models()
                print("best_", best_pycaret_model)
                y_pred = best_pycaret_model.predict(X_test)
                score = r2_score(y_test, y_pred)
        elif operation_type.lower() == "clustering":
            # For clustering, y and target are not used
            with open(os.devnull, 'w') as devnull, \
                contextlib.redirect_stdout(devnull), \
                contextlib.redirect_stderr(devnull):
                setup_cluster(data=X, session_id=42, silent=True)
                # Use KMeans as default, or allow user to specify
                model = create_cluster_model('kmeans')
                cluster_labels = assign_cluster_model(model, X)['Cluster']
                # Silhouette score as main metric
                if len(set(cluster_labels)) > 1:
                    score = silhouette_score(X, cluster_labels)
                else:
                    score = 0.0
                best_pycaret_model = model
                y_pred = cluster_labels
        else:
            raise ValueError(f"Unsupported operation type: {operation_type}")

        print("best_pycaret_model:", best_pycaret_model)
        return score, y_pred, best_pycaret_model
    except Exception as e:
        print(f"pycaret failed: {e}")
        return None, None, None
    finally:
        print("pycaret ended")

