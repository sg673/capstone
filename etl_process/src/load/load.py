import pandas as pd
from src.load.load_database import load_to_database


def load_main(data: pd.DataFrame):
    
    load_to_database(data, "replace")