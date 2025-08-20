from enum import Enum
from pathlib import Path
import pandas as pd
import os


class AccessType(Enum):
    DATABASE = 1
    FILE = 2
    ETL = 3


def get_data(access: AccessType = AccessType.DATABASE) -> pd.DataFrame:
    if access == AccessType.DATABASE:
        # Add connection to database
        print("not availabe yet")
        return pd.DataFrame()

    if access == AccessType.FILE:
        file = Path(os.getcwd()).parent / "etl_process" / "data" / "output" / "merged_data.csv"
        if not file.exists():
            raise FileNotFoundError(f"file not found {file}")
        df = pd.read_csv(file, encoding="latin-1", index_col=0)
        return df

    if access == AccessType.ETL:
        # run the etl pipeline and get the dataframe directly
        print("not availabe yet")
        return pd.DataFrame()
