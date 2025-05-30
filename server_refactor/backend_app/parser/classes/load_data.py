import os
import pickle
import pandas as pd
def load_saved_model(model_name,response):
    url = os.path.join(os.path.dirname(__file__), f"../model/{model_name}.pkl")
    try:
        with open(url, 'rb') as file:
            model = pickle.load(file)
        return model, response
    except FileNotFoundError:
        response["error"] = f"Model: [{model_name}] Not found."
        return None, response
    except Exception as e:
        response["error"] = f"An error occurred while loading the model: {str(e)}"
        return None, response
    
def load_over_df(df_name):
    url = os.path.join(os.path.dirname(__file__), f"../../data/files/{df_name}.csv")
    return pd.read_csv(url)