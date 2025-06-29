from sklearn.metrics import accuracy_score, r2_score
from tpot import TPOTRegressor, TPOTClassifier

# from auto_sklearn2 import AutoSklearnClassifier
# from auto_sklearn2 import AutoSklearnRegressor
# from auto_sklearn2 import AutoSklearnClassifier, AutoSklearnRegressor

# TPOT AutoML implementation

def tpot(operation_type, X_train, y_train, X_test, y_test):
    if operation_type.upper() == "CLUSTERING":
        print("TPOT does not support clustering. Returning None.")
        return None, None, None
    if operation_type.upper() == "PREDICTION":
        model = TPOTRegressor(generations=2, population_size=5, verbosity=2)
    elif operation_type.upper() == "CLASSIFICATION":
        model = TPOTClassifier(generations=1, population_size=1, verbosity=1)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    if operation_type.upper() == "CLASSIFICATION":
        score = accuracy_score(y_test, y_pred)
    else:
        score = r2_score(y_test, y_pred)
    model_name = str(model.fitted_pipeline_.steps[0][1])
    return  score, y_pred, model_name