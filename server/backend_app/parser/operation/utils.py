import os
import pickle
import pandas as pd
import uuid
from sqlalchemy import create_engine
from django.core.files.base import ContentFile
from django.conf import settings

from ...models import MLModel

import json
class TempGenerateError(Exception):
    pass

def get_env_var(key):
    return os.getenv(key)

def safe_remove_features(features, to_remove):
    return [f for f in features if f not in to_remove] 

def get_connection():
    connection_string = get_env_var("POSTGRES_URL")
    if not connection_string:
        raise TempGenerateError("POSTGRES_URL environment variable not set.")
    return create_engine(connection_string)

def get_arg(command_parts, key, default=None, offset=1):
    try:
        idx = [p.upper() for p in command_parts].index(key.upper())
        arg = command_parts[idx + offset]
        while '"' in arg:
            arg = arg.replace('"', '')
            next_arg = command_parts[idx + offset + 1]
            if next_arg.endswith('"'):
                return arg + ' ' + next_arg.replace('"', '')
            arg += ' ' + next_arg
            offset += 1
        return arg
    except (ValueError, IndexError):
        return default


def is_flag_present(command_parts, key):
    return key.upper() in [p.upper() for p in command_parts]


def parse_features(df, feature_str):
    return df.columns.tolist() if '*' in feature_str else feature_str.split(',')



def parse_command_parts(command):
    return [part for part in command.split(" ") if part.strip()]

def get_operation_type(command_parts):
    types = ["PREDICTION", "CLASSIFICATION", "CLUSTERING"]
    return next((t for t in types if t in map(str.upper, command_parts)), "PREDICTION")

def get_dataset_name(command_parts):
    try:
        return command_parts[[p.upper() for p in command_parts].index("FROM") + 1].split(';')[0]
    except Exception:
        raise TempGenerateError("Dataset name not found in command.")

def get_features(command_parts, df, over_df=None):
    try:
        feature_part = command_parts[[p.upper() for p in command_parts].index("FEATURES") + 1].strip()
        if "OVER" in map(str.upper, command_parts) and over_df is not None:
            return over_df.columns.tolist() if '*' in feature_part else feature_part.split(',')
        return df.columns.tolist() if '*' in feature_part else feature_part.split(',')
    except Exception:
        raise TempGenerateError("Features not found in command.")

def get_target(command_parts, operation_type):
    try:
        idx = [p.upper() for p in command_parts].index(operation_type.upper()) + 1
        return command_parts[idx]
    except Exception:
        raise TempGenerateError(f"Target not found for operation {operation_type}.")



def save_model_pickle(model, user, dataset_name, framework, command, best_pycaret_model=None):
    if not user:
        return None

    dataset_base = os.path.splitext(os.path.basename(dataset_name))[0]
    model_filename = f"{dataset_base}_{framework}.pkl"

    # Special case for H2O
    if framework.lower() == "h2o":
        # Use H2O's native save_model function
        import h2o
        model_dir = os.path.join(settings.MEDIA_ROOT, "h2o_models", f"user_{user.id}")
        os.makedirs(model_dir, exist_ok=True)
        try:
            h2o_path = model.save_model(path=model_dir, force=True)
        except:
            h2o_path = "N/A"
        MLModel.objects.create(
            user=user,
            name=os.path.basename(h2o_path),
            model_file=None,  
            algorithm=framework,
            table_used=dataset_base,
            query=command
        )
        return h2o_path 

    # TPOT special-case
    if framework.lower() == "tpot" and hasattr(model, "fitted_pipeline_"):
        model_to_save = model.fitted_pipeline_
    elif framework.lower() == "pycaret":
        # if best_pycaret_model is None:
            # raise ValueError("For PyCaret, best_pycaret_model must be provided.")
        model_to_save =  model #best_pycaret_model
    else:
        model_to_save = model

    try:
        model_bytes = pickle.dumps(model_to_save)
    except Exception as e:
        raise ValueError(f"Failed to pickle model for {framework}.") from e

    django_file = ContentFile(model_bytes)
    django_file.name = model_filename

    MLModel.objects.create(
        user=user,
        name=model_filename,
        model_file=django_file,
        algorithm=framework,
        table_used=dataset_base,
        query=command
    )

    return f"user_{user.id}/{framework}/{model_filename}"

