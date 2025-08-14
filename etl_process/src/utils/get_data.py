import pandas as pd
from pathlib import Path
from src.utils.logging_utils import setup_logger, log_extract_success
import logging
import timeit

logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)


def get_raw_file(fileName: str) -> pd.DataFrame:
    """
        Extracts a CSV file from the raw data folder and loads it into a pandas
        DataFrame.

        Args:
            fileName (str): The name of the CSV file to be loaded from the
            '../../data/raw/' directory.
        Returns:
            pd.DataFrame: The contents of the CSV file as a pandas
            DataFrame.
        Raises:
            FileNotFoundError: If the specified file does not exist in the
            raw data folder.
            Exception: If there is an error reading the file (e.g., parsing
            error, permission error).
        Example:
            df = get_raw_file("data.csv")
    """

    start_time = timeit.default_timer()
    data_path = Path(__file__).parent.parent.parent / "data" / "raw" / fileName

    try:
        df = pd.read_csv(data_path)
        extract_file_execution_time = timeit.default_timer() - start_time
        log_extract_success(
            logger,
            fileName[:-4] + " from CSV",
            df.shape,
            extract_file_execution_time,
            0.0001
        )
        return df
    except FileNotFoundError:
        logger.setLevel(logging.ERROR)
        logger.error(f"File {fileName} not found in {data_path}")
        raise FileNotFoundError(
            f"File {fileName} not found in {data_path}"
        )
    except Exception as e:
        logger.setLevel(logging.ERROR)
        logger.error(f"Error reading file {fileName}: {str(e)}")
        raise Exception(f"Error reading file {fileName}: {str(e)}")
