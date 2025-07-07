import os
import pickle
import pandas as pd
import uuid
from sklearn.metrics import accuracy_score, r2_score, silhouette_score

import json

def h2o(X_train, X_test, y_train, y_test, target, operation_type, features, n_clusters=3):
    print("h2o started")
    try:
        import h2o
        from h2o.automl import H2OAutoML
        from h2o.estimators.kmeans import H2OKMeansEstimator
        h2o.init(verbose=False)
        train_df = X_train.copy()
        if operation_type.lower() == "clustering":
            train_h2o = h2o.H2OFrame(train_df)
            k = n_clusters if n_clusters else 3
            if hasattr(X_train, 'shape'):
                k = min(k, X_train.shape[0])
            model = H2OKMeansEstimator(k=k, seed=42)
            model.train(x=features, training_frame=train_h2o)
            cluster_labels = model.predict(train_h2o).as_data_frame().iloc[:, 0]
            # Silhouette score as main metric
            if len(set(cluster_labels)) > 1:
                score = silhouette_score(X_train, cluster_labels)
            else:
                score = 0.0
            return score, list(cluster_labels), model
        else:
            test_df = X_test.copy()
            test_df[target] = y_test
            train_df[target] = y_train
            train_h2o = h2o.H2OFrame(train_df)
            test_h2o = h2o.H2OFrame(X_test.copy())
            if operation_type.lower() == "classification":
                train_h2o[target] = train_h2o[target].asfactor()
                aml = H2OAutoML(max_runtime_secs=120, seed=42)
                aml.train(x=features, y=target, training_frame=train_h2o)
                y_pred = aml.leader.predict(test_h2o).as_data_frame().iloc[:, 0]
                score = accuracy_score(y_test, y_pred)
            elif operation_type.lower() == "prediction":
                aml = H2OAutoML(max_runtime_secs=120, seed=42)
                aml.train(x=features, y=target, training_frame=train_h2o)
                y_pred = aml.leader.predict(test_h2o).as_data_frame().iloc[:, 0]
                score = r2_score(y_test, y_pred)
            else:
                raise ValueError(f"Unsupported operation type: {operation_type}")
            print("aml.leader:", aml.leader)
            print("aml.leader.model_id:", aml.leader.model_id)
            print("Test H2O columns:", test_h2o.columns)
            print("Train H2O columns:", train_h2o.columns)
            return score, list(y_pred), aml.leader.model_id
    except Exception as e:
        print(f"h2o failed: {e}")
        return None, None, None
    finally:
        try:
            h2o.cluster().shutdown(prompt=False)
        except Exception:
            print("Failed to shutdown H2O cluster gracefully.")
        print("h2o ended")          
