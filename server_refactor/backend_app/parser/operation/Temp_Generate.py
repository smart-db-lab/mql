import os
import pandas as pd
import uuid
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.compose import ColumnTransformer
from django.conf import settings

from .Clustering import clustering_generate

from ..Function.display_result import display_results
from ..Function.select_algorithm import select_algorithm
from ..classes.load_data import load_over_df
from ..classes.dl_algo import train_and_evaluate_sklearn

from .utils import save_model_pickle, get_connection, get_arg, is_flag_present, parse_features, parse_command_parts, get_operation_type

def temp_generate(command, user=None):
    command_parts = command.strip().split()
    response = {'text': [], 'graph': '', 'table': '', 'query': command}
    operation_type = next((t for t in ["PREDICTION", "CLASSIFICATION", "CLUSTERING"]
                           if t in map(str.upper, command_parts)), "PREDICTION")
    dataset_name = get_arg(command_parts, "FROM", "").split(';')[0]

    # Load dataset
    try:
        conn = get_connection()
        df = pd.read_sql_query(f'SELECT * FROM "{dataset_name}"', conn)
    except Exception as e:
        response['text'] = f"Error loading dataset: {e}"
        return response

    feature_str = get_arg(command_parts, "FEATURES", "")
    Over_df = load_over_df(get_arg(command_parts, "OVER", "").split(';')[0]) if is_flag_present(command_parts, "OVER") else None
    features = parse_features(Over_df if Over_df is not None else df, feature_str)
    target = get_arg(command_parts, operation_type)

    if operation_type.upper() == "CLUSTERING":
        return clustering_generate(command, user)
    
    if target in features:
        features.remove(target)

    y = df[target]
    if operation_type.upper() == "CLASSIFICATION":
        y = pd.Series(LabelEncoder().fit_transform(y), name=target)

    X = df[features]
    
    # Encode categorical features for classification
    if operation_type.upper() == "CLASSIFICATION":
        # Identify categorical columns
        categorical_columns = X.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if categorical_columns:
            # Use OneHotEncoder for categorical features
            preprocessor = ColumnTransformer(
                transformers=[
                    ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_columns),
                    ('num', 'passthrough', [col for col in X.columns if col not in categorical_columns])
                ],
                remainder='passthrough'
            )
            print(f"Categorical Feature found ! Encoding categorical features: {categorical_columns}")
            X_encoded = preprocessor.fit_transform(X)
            
            # Get feature names after encoding
            cat_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_columns)
            num_feature_names = [col for col in X.columns if col not in categorical_columns]
            features = list(cat_feature_names) + list(num_feature_names)
            
            X = pd.DataFrame(X_encoded, columns=features, index=X.index)
    
    test_size = float(get_arg(command_parts, "TEST", 20, offset=2)) / 100
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

    # Build model set
    models = {
        'pycaret': None, 
        'sklearn': select_algorithm(operation_type, get_arg(command_parts, "ALGORITHM", "")),
        'tpot': None,
        'autosklearn2': None,  
        'h2o': None
    }

    results = {}
    y_preds = {}
    best_pycaret_model = None
    # === Start automl section ===
    from ..auto_ml.pycaret import pycaret
    try:
        results['pycaret'],y_preds['pycaret'],models['pycaret'] = pycaret(X, y, X_test, y_test, target, operation_type)
    except Exception as e:
        print(f"pycaret failed: {e}")
        pass
 
    try:
        from ..auto_ml.h2o import h2o
        results['h2o'],y_preds['h2o'],models['h2o'] = h2o(X_train, X_test, y_train, y_test, target, operation_type,features)
    except Exception as e:
        print(f"h2o failed: {e}")
        pass
   
    # from ..auto_ml.autosklearn2 import autosklearn2
    # results['autosklearn2'], y_preds['autosklearn2'],models['autosklearn2']  = autosklearn2(X_train, y_train, X_test, y_test, operation_type, y_preds, models)
    
    
    try:
        from ..auto_ml.tpot import tpot
        results['tpot'], y_preds['tpot'], models['tpot'] = tpot(operation_type, X_train, y_train, X_test, y_test)
    except Exception as e:
        print(f"tpot failed: {e}")
        pass


    # === End automl section ===
    

    # sklearn
    for name in ['sklearn']:
        try:
            model = models[name]
            # print(f"Training {name} model...",y)
            y_preds[name], results[name] = train_and_evaluate_sklearn(model, X_train, X_test, y_train, y_test, operation_type)
            # print(f"{name} trained successfully with score: {results[name]}")
        except Exception as e:
            print(f"{name} failed: {e}")
            response['text'].append(f"Error training {name} model: {e}")


    if not results:
        response['text'].append("No models trained successfully.")
        return response
    print(f"Results: {results}")
    valid_results = {k: v for k, v in results.items() if isinstance(v, (int, float)) and v is not None}
    if not valid_results:
        response['text'].append("No valid model scores available.")
        return response
    best_framework = max(valid_results, key=valid_results.get)
    best_score = results[best_framework]
    best_model = models[best_framework]

    best_pred = pd.DataFrame({'Predicted': list(y_preds[best_framework])})

    df_result = pd.concat([X_test.reset_index(drop=True), y_test.reset_index(drop=True), best_pred.reset_index(drop=True)], axis=1)

    if is_flag_present(command_parts, "LABEL"):
        label = get_arg(command_parts, "LABEL")
        df_result.insert(0, label, range(1, len(df_result) + 1))

    table_dir = os.path.join(settings.MEDIA_ROOT, "tables")
    os.makedirs(table_dir, exist_ok=True)

    table_filename = f"table_{uuid.uuid4().hex}.csv"
    result_path = os.path.join(table_dir, table_filename)

    df_result.to_csv(result_path, index=False)
    response['table'] = df_result.replace([float('inf'), float('-inf'), float('nan')], None).to_dict(orient='records')

    response['text'].append(f"Best Model: {best_framework} with score {best_score:.4f}")

    # Performance Table
    performance_table = []
    for framework, score in results.items():
        entry = {"Framework": framework, "Score": round(score, 4)} if score is not None else {"Framework": framework, "Score": "N/A"}
        entry["Algorithm"] = str(models[framework])
        performance_table.append(entry)

    performance_table.sort(key=lambda x: (x["Score"] == "N/A", x["Score"]), reverse=True)
    response["performance_table"] = performance_table

    # Save best model
    model_path = save_model_pickle(
        best_model, user, dataset_name, best_framework, command,
        best_pycaret_model=best_pycaret_model if best_framework == "pycaret" else None
    )

    # Optional graph
    if is_flag_present(command_parts, "DISPLAY"):
        response['graph'], response['graph_link'], response['graph_path'] = display_results(
            operation_type, y_test, best_pred, best_model, features, df
        )
        print(f"Graph generated: {response['graph_link']}, {response['graph_path']}")

    return response
