import pandas as pd
from src.utils.logging_utils import setup_logger
import logging

logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)


def clean_delay_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    """

    duplicated_rows = data.duplicated()
    logger.info(f"Detected {duplicated_rows.sum()} duplicate rows")
    clean_data = data[~duplicated_rows]

    clean_data.columns = clean_data \
        .columns \
        .str.lower() \
        .str.replace(" ", "_")

    CRITICAL_COLUMNS = ['year',
                        'month',
                        'carrier',
                        'carrier_name',
                        'airport',
                        'airport_name']
    clean_data = clean_data.dropna(subset=CRITICAL_COLUMNS)
    clean_data = clean_data.fillna(0)


    return clean_data
