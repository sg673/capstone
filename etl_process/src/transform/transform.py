import pandas as pd

from src.transform.clean_delay import clean_delay_data
from src.utils.logging_utils import setup_logger
import logging

logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)


def transform_main(data: "tuple[pd.DataFrame,pd.DataFrame]") -> "tuple[pd.DataFrame,pd.DataFrame]":
    """
    """
    clean_airport = pd.DataFrame()
    clean_delay = clean_delay_data(data[1])

    logger.info(f"Transform completed successfully - "
                f"Airports: {clean_airport.shape},"
                f"Delays: {clean_delay.shape}")

    return (clean_airport, clean_delay)
