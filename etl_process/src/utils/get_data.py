import pandas as pd
from pathlib import Path


def get_raw_file(fileName: str) -> pd.DataFrame:
    """
        Extracts a CSV file from the raw data folder and loads it into a pandas DataFrame.
        Args:
            fileName (str): The name of the CSV file to be loaded from the '../../data/raw/' directory.
        Returns:
            pd.DataFrame: The contents of the CSV file as a pandas DataFrame.
        Raises:
            FileNotFoundError: If the specified file does not exist in the raw data folder.
            Exception: If there is an error reading the file (e.g., parsing error, permission error).
        Example:
            df = get_raw_file("data.csv")
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
