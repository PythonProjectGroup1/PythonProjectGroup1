from pathlib import Path
import yaml
import pandas as pd
from paths import API_CONFIG_DIR

def load_config(path) -> dict:
    config_path = path.resolve()
    with open(config_path, "r") as file:
        return yaml.safe_load(file)
    
def fetch_csv(path):
    try: 
        with open(path, 'r') as csv:
            df = pd.read_csv(csv)
            # print(f"Fetched saved CSV at {path}")
            # print(df.head())
            return df
    except FileNotFoundError:
        print(f"CSV File Not found at {path}")
    except Exception as e:
        print(f"Error: {e}")
