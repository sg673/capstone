import pandas as pd


def get_raw_file(fileName: str) -> pd.DataFrame:
    """
    Extracts a file from the raw folder and converts it into a DataFrame.
    """
    try:
        return pd.read_csv(f"../../data/raw/{fileName}")
    except FileNotFoundError:
        raise FileNotFoundError(
            f"File {fileName} not found in raw data folder"
        )
    except Exception as e:
        raise Exception(f"Error reading file {fileName}: {str(e)}")
