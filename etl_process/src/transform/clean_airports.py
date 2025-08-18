import pandas as pd
from src.utils.logging_utils import setup_logger
import logging

logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)


def clean_airport_data(data: pd.DataFrame) -> pd.DataFrame:
    """
    """
    duplicated_rows = data.duplicated()
    logger.info(f"Detected {duplicated_rows.sum()} duplicate rows")
    clean_data = data[~duplicated_rows]
    logger.info("Duplicates removed successfully")

    clean_data.columns = clean_data \
        .columns \
        .str.lower() \
        .str.replace(" ", "_")

    logger.info("Column names formatted")
    CRITICAL_COLUMNS = ['name',
                        'iata']
    rows_before_drop = len(clean_data)
    clean_data = clean_data.dropna(subset=CRITICAL_COLUMNS)
    rows_dropped = rows_before_drop - len(clean_data)

    rows_before_fill = len(clean_data)
    clean_data['city'] = clean_data['city'].fillna("No City Provided")
    clean_data = clean_data.fillna(0)
    rows_modified = rows_before_fill - len(clean_data)
    logger.info(f"Dropped {rows_dropped} rows with critical nulls, filled "
                f"nulls in {rows_modified} rows")

    # arrays are AI generated
    str_cols = ['name',
                'iata',
                'city']
    float_cols = ['lat',
                  'lon',
                  'alt']
    clean_data[str_cols] = clean_data[str_cols].astype("string")
    clean_data[float_cols] = clean_data[float_cols].astype("float64")
    logger.info("columns converted to correct datatypes")

    return clean_data
