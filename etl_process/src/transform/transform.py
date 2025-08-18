import pandas as pd

from src.transform.merge import merge_main
from src.transform.transformer import Transformer
from src.utils.post_data import post
from src.utils.logging_utils import setup_logger
import logging

logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)

# Add these constants at the top of the file after the logger setup:

AIRPORT_CONFIG = {
    "crit_cols": ["name", "iata"],
    "col_types": {
        "str_cols": ["name", "iata", "city"],
        "float_cols": ["lat", "lon", "alt"],
        "int_cols": []
    }
}

DELAY_CONFIG = {
    "crit_cols": ["year", "month",
                  "carrier", "carrier_name",
                  "airport", "airport_name"],
    "col_types": {
        "str_cols": ["carrier", "carrier_name",
                     "airport", "airport_name"],
        "int_cols": ["year", "month", "arr_flights",
                     "arr_del15", "arr_cancelled",
                     "arr_diverted", "arr_delay",
                     "carrier_delay", "weather_delay",
                     "nas_delay", "security_delay",
                     "late_aircraft_delay"],
        "float_cols": ["carrier_ct", "weather_ct",
                       "nas_ct", "security_ct",
                       "late_aircraft_ct"]
    }
}


def transform_main(data: "tuple[pd.DataFrame,pd.DataFrame]",
                   write_to_file=False) -> pd.DataFrame:
    """
        Transform raw airport and delay data by cleaning and preprocessing
        both datasets.

        Args:
            data (tuple[pd.DataFrame, pd.DataFrame]): Tuple containing raw
            airport and delay data

            write_to_file (bool, optional): Whether to write cleaned data to
            CSV files. Defaults to False.

        Returns:
            pd.DataFrame: Cleaned and merged data
    """

    airport_cleaner = Transformer(data[0],
                                  AIRPORT_CONFIG["crit_cols"],
                                  AIRPORT_CONFIG["col_types"])
    delay_cleaner = Transformer(data[1],
                                DELAY_CONFIG["crit_cols"],
                                DELAY_CONFIG["col_types"])
    logger.info("Started cleaning airports")
    clean_airport = airport_cleaner.clean()
    logger.info("airports cleaned")
    logger.info("Started cleaning delays")
    clean_delay = delay_cleaner.clean()
    logger.info("delays cleaned")

    logger.info(f"Transform completed successfully - "
                f"Airports: {clean_airport.shape},"
                f"Delays: {clean_delay.shape}")

    logger.info("starting merge")
    merged_data = merge_main(clean_airport, clean_delay)
    logger.info(f"Completed merge - "
                f"Merged Data: {merged_data.shape}")

    if write_to_file:
        post("output", "clean_airports.csv", clean_airport)
        post("output", "clean_delay.csv", clean_delay)
        post("output", "merged_data.csv", merged_data)

    return merged_data
