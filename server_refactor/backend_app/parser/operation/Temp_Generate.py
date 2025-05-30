import os
import json
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, r2_score
from sqlalchemy import create_engine
from sklearn.preprocessing import LabelEncoder
from django.core.files import File
from django.conf import settings

from ..Function.Clustering import Clustering
from ..Function.display_result import display_results
from ..Function.select_algorithm import select_algorithm
from ..classes.load_data import load_over_df
from ..classes.dl_algo import train_and_evaluate_auto_ml, train_and_evaluate_sklearn
from ...models  import MLModel  # Assuming MLModel exists and has relevant fields

def get_arg(command_parts, key, default=None, offset=1):
    try:
        idx = [p.upper() for p in command_parts].index(key.upper())
        return command_parts[idx + offset]
    except (ValueError, IndexError):
        return default

def is_flag_present(command_parts, key):
    return key.upper() in [p.upper() for p in command_parts]

def parse_features(df, feature_str):
    return df.columns.tolist() if '*' in feature_str else feature_str.split(',')

from django.core.files.base import ContentFile
from django.core.files.base import ContentFile
import os
import pickle

def save_model_pickle(model, user, dataset_name, framework, command, best_pycaret_model=None):
    if not user:
        return None

    dataset_base = os.path.splitext(os.path.basename(dataset_name))[0]
    model_filename = f"{dataset_base}_{framework}.pkl"

    # Safely extract serializable pipeline depending on framework
    if framework.lower() == "tpot":
        if hasattr(model, "fitted_pipeline_"):
            model_to_save = model.fitted_pipeline_
        else:
            raise ValueError("TPOT model has no fitted pipeline. Did you forget to fit it?")

    elif framework.lower() == "pycaret":
        # Only save model returned by compare_models()
        if best_pycaret_model is not None:
            model_to_save = best_pycaret_model
        else:
            raise ValueError("For PyCaret, please pass the model returned by compare_models().")
    else:
        model_to_save = model  # sklearn or others

    # Try serializing the model
    try:
        model_bytes = pickle.dumps(model_to_save)
    except Exception as e:
        raise ValueError(f"Failed to pickle model for {framework}. Ensure it's a plain scikit-learn pipeline.") from e

    # Wrap as Django file
    django_file = ContentFile(model_bytes)
    django_file.name = model_filename

    # Save in database
    MLModel.objects.create(
        user=user,
        name=model_filename,
        model_file=django_file,
        algorithm=framework,
        table_used=dataset_base,
        query=command
    )

    return f"user_{user.id}/{framework}/{model_filename}"

from pycaret.classification import compare_models as compare_classification_models
from pycaret.regression import compare_models as compare_regression_models


def temp_generate(command, user=None):
    command_parts = command.strip().split()
    response = {'text': [], 'graph': '', 'table': '', 'query': command}
    operation_type = next((t for t in ["PREDICTION", "CLASSIFICATION", "CLUSTERING"] if t in map(str.upper, command_parts)), "PREDICTION")
    dataset_name = get_arg(command_parts, "FROM", "").split(';')[0]

    # Load dataset
    try:
        conn = create_engine(os.getenv("POSTGRES_URL"))
        df = pd.read_sql_query(f'SELECT * FROM "{dataset_name}"', conn)
    except Exception as e:
        response['text'] = f"Error loading dataset: {e}"
        return response

    # Features and target
    feature_str = get_arg(command_parts, "FEATURES", "")
    Over_df = load_over_df(get_arg(command_parts, "OVER", "").split(';')[0]) if is_flag_present(command_parts, "OVER") else None
    features = parse_features(Over_df if Over_df is not None else df, feature_str)
    target = get_arg(command_parts, operation_type)

    if target in features:
        features.remove(target)

    y = df[target]
    if operation_type.upper() == "CLASSIFICATION":
        y = pd.Series(LabelEncoder().fit_transform(y), name=target)

    X = df[features]
    test_size = float(get_arg(command_parts, "TEST", 20, offset=2)) / 100
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    # Build models
    models = {
        'pycaret': select_algorithm(operation_type, "pycaret", data=pd.concat([X, y], axis=1), target=target),
        'sklearn': select_algorithm(operation_type, get_arg(command_parts, "ALGORITHM", "")),
        'tpot': select_algorithm(operation_type, "tpot"),
    }

    results = {}
    y_preds = {}
    best_pycaret_model = None

    for name, model in models.items():
        try:
            if name == "pycaret":
                if operation_type.lower() == "classification":
                    best_pycaret_model = compare_classification_models()
                else:
                    best_pycaret_model = compare_regression_models()

                # Predict using the best PyCaret model
                y_pred = best_pycaret_model.predict(X_test)
                if operation_type.lower() == "classification":
                    score = accuracy_score(y_test, y_pred)
                else:
                    score = r2_score(y_test, y_pred)

                models[name] = best_pycaret_model  # Replace for consistency
                y_preds[name] = y_pred
                results[name] = score

            else:
                y_pred, score = train_and_evaluate_auto_ml(model, X_train, X_test, y_train, y_test, operation_type)
                y_preds[name] = y_pred
                results[name] = score

        except Exception as e:
            print(f"{name} failed: {e}")

    if not results:
        response['text'].append("No models trained successfully.")
        return response

    best_framework = max(results, key=results.get)
    best_score = results[best_framework]
    best_model = models[best_framework]
    best_pred = pd.DataFrame(y_preds[best_framework], index=y_test.index, columns=["Predicted"])

    # Result table
    df_result = pd.concat([X_test.reset_index(drop=True), y_test.reset_index(drop=True), best_pred.reset_index(drop=True)], axis=1)
    if is_flag_present(command_parts, "LABEL"):
        label = get_arg(command_parts, "LABEL")
        df_result.insert(0, label, range(1, len(df_result) + 1))

    result_path = os.path.join(os.path.dirname(__file__), "../table/table_.csv")
    df_result.to_csv(result_path, index=False)
    response['table'] = df_result.to_dict(orient='records')
    response['text'].append(f"Best Model: {best_framework} with score {best_score}")

    # Save best model
    model_path = save_model_pickle(
        best_model, user, dataset_name, best_framework, command,
        best_pycaret_model=best_pycaret_model if best_framework == "pycaret" and best_pycaret_model is not None else None
    )
    if model_path:
        response['text'].append(f"Model saved to {model_path}")

    # Optional graph
    if is_flag_present(command_parts, "DISPLAY"):
        response['graph'], response['graph_link'] ,response['graph_path']= display_results(operation_type, y_test, best_pred, best_model, features, df)
        print(f"Graph generated: {response['graph_link']}, {response['graph_path']}")
    return response
