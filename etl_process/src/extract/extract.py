import pandas as pd
from src.extract.get_delay_data import extract_delay_data
from src.extract.get_airports import extract_airport_locations
from src.utils.logging_utils import setup_logger
import logging

logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)


def extract_main() -> "tuple[pd.DataFrame, pd.DataFrame]":
    """
        Runs the extraction phase
    """
    airports = extract_airport_locations()
    delay_info = extract_delay_data()
    logger.info(f"Extraction completed successfully - "
                f"Airports: {airports.shape}, Delays: {delay_info.shape}")

    return (airports, delay_info)
