import os
from sqlalchemy import create_engine

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
