import pandas as pd
from src.utils.logging_utils import setup_logger
import logging

logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)


def clean_airport_data(data: pd.DataFrame) -> pd.DataFrame:
    """
        Clean and preprocess airport data by removing duplicates,
        handling nulls,
        and converting data types.

        Args:
            data (pd.DataFrame): Raw airport data

        Returns:
            pd.DataFrame: Cleaned airport data with proper data types
    """

    duplicated_rows = data.duplicated()
    clean_data = data[~duplicated_rows]
    logger.info(f"Removed {duplicated_rows.sum()} duplicate rows")

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

    rows_with_nulls = clean_data.isna().any(axis=1).sum()
    nulls_before_fill = clean_data.isna().sum().sum()
    clean_data['city'] = clean_data['city'].fillna("No City Provided")
    clean_data = clean_data.fillna(0)
    nulls_after_fill = clean_data.isna().sum().sum()
    if nulls_after_fill == 0:
        logger.info(f"Dropped {rows_dropped} rows with critical nulls, filled "
                    f"{nulls_before_fill} nulls in {rows_with_nulls} rows")
    else:
        logger.warning(f"could not handle {nulls_after_fill} nulls")

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
