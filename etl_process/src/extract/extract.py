import pandas as pd
from src.extract.get_delay_data import extract_delay_data
from src.extract.get_airports import extract_airport_locations
from src.utils.logging_utils import setup_logger
from src.utils.post_data import post
import logging

logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)


def extract_main(write_to_file=False) -> "tuple[pd.DataFrame, pd.DataFrame]":
    """
        Runs the extraction phase

        args:
            write_to_file: whether to write the output to a file
    """
    airports = extract_airport_locations()
    delay_info = extract_delay_data()
    logger.info(f"Extraction completed successfully - "
                f"Airports: {airports.shape}, Delays: {delay_info.shape}")

    if write_to_file:
        post("processed", "extract_airports.csv", airports)
        post("processed", "extract_delay.csv", delay_info)

    return (airports, delay_info)
