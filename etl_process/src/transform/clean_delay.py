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

    # arrays are AI generated
    str_cols = ['carrier',
                'carrier_name',
                'airport',
                'airport_name']
    int_cols = ['year',
                'month',
                'arr_flights',
                'arr_del15',
                'arr_cancelled',
                'arr_diverted',
                'arr_delay',
                'carrier_delay',
                'weather_delay',
                'nas_delay',
                'security_delay',
                'late_aircraft_delay']
    float_cols = ['carrier_ct',
                  'weather_ct',
                  'nas_ct',
                  'security_ct',
                  'late_aircraft_ct']
    clean_data[str_cols] = clean_data[str_cols].astype("string")
    clean_data[int_cols] = clean_data[int_cols].astype("int64")
    clean_data[float_cols] = clean_data[float_cols].astype("float64")

    return clean_data
