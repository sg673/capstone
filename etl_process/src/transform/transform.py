import pandas as pd

from src.utils.post_data import post
from src.transform.clean_airports import clean_airport_data
from src.transform.clean_delay import clean_delay_data
from src.utils.logging_utils import setup_logger
import logging

logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)


def transform_main(data: "tuple[pd.DataFrame,pd.DataFrame]",
                   write_to_file=False) -> "tuple[pd.DataFrame,pd.DataFrame]":
    """
        Transform raw airport and delay data by cleaning and preprocessing
        both datasets.

        Args:
            data (tuple[pd.DataFrame, pd.DataFrame]): Tuple containing raw
            airport and delay data

            write_to_file (bool, optional): Whether to write cleaned data to
            CSV files. Defaults to False.

        Returns:
            tuple[pd.DataFrame, pd.DataFrame]: Tuple containing cleaned
            airport and delay data
    """

    clean_airport = clean_airport_data(data[0])
    clean_delay = clean_delay_data(data[1])

    logger.info(f"Transform completed successfully - "
                f"Airports: {clean_airport.shape},"
                f"Delays: {clean_delay.shape}")

    if write_to_file:
        post("output", "extract_airports.csv", clean_airport)
        post("output", "extract_delay.csv", clean_delay)

    return (clean_airport, clean_delay)
