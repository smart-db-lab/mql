# # AutoSklearn2
from sklearn.metrics import accuracy_score, r2_score
# import pandas as pd

def autosklearn2(X_train, y_train, X_test, y_test, operation_type, results=None, y_preds=None, models=None):
    if operation_type.lower() == "clustering":
        print("AutoSklearn2 does not support clustering. Returning None.")
        return None, None, None
    try:
        from autosklearn.classification import AutoSklearnClassifier
        from autosklearn.regression import AutoSklearnRegressor
        if operation_type.lower() == "classification":
            autosklearn_model = AutoSklearnClassifier()
            autosklearn_model.fit(X_train, y_train)
            y_pred = autosklearn_model.predict(X_test)
            score = accuracy_score(y_test, y_pred)
        else:
            autosklearn_model = AutoSklearnRegressor()
            autosklearn_model.fit(X_train, y_train)
            y_pred = autosklearn_model.predict(X_test)
            score = r2_score(y_test, y_pred)
        return score, y_pred, autosklearn_model
    except Exception as e:
        print(f"autosklearn2 failed: {e}")
        return None, None, None
