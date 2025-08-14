import pandas as pd
from pathlib import Path


def get_raw_file(fileName: str) -> pd.DataFrame:
    """
        Extracts a CSV file from the raw data folder and loads it into a pandas DataFrame.
    """
    data_path = Path(__file__).parent.parent.parent / "data" / "raw" / fileName
    try:
        return pd.read_csv(data_path)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"File {fileName} not found in {data_path}"
        )
    except Exception as e:
        raise Exception(f"Error reading file {fileName}: {str(e)}")
