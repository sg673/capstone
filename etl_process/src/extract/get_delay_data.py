from src.utils.get_data import get_raw_file
import pandas as pd
from src.utils.logging_utils import setup_logger
import logging

logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)


def extract_delay_data() -> pd.DataFrame:
    """
        Extracts and processes airline delay data from CSV file.

        Returns:
            pd.DataFrame: DataFrame with airline delay information including:
                - year, month: Time period
                - carrier, carrier_name: Airline information
                - airport IATA, airport_name: Airport information
                - Various delay metrics and counts

        Raises:
            FileNotFoundError: If the delay data file doesn't exist
            KeyError: If expected columns are missing
            ValueError: If no data is extracted
    """
    EXPECTED_SCHEMA = [
        "year",
        "month",
        "carrier",
        "carrier_name",
        "airport",
        "airport_name",
        "arr_flights",
        "arr_del15",
        "carrier_ct",
        "weather_ct",
        "nas_ct",
        "security_ct",
        "late_aircraft_ct",
        "arr_cancelled",
        "arr_diverted",
        "arr_delay",
        "carrier_delay",
        "weather_delay",
        "nas_delay",
        "security_delay",
        "late_aircraft_delay"
    ]

    delay_df = get_raw_file("Airline_Delay_Cause.csv")

    # Validate schema
    missing_columns = set(EXPECTED_SCHEMA) - set(delay_df.columns)
    if missing_columns:
        logger.setLevel(logging.ERROR)
        logger.error(
            f"Missing expected columns in delays: {missing_columns}"
        )
        raise KeyError(f"Missing expected columns: {missing_columns}")

    delay_df = delay_df.sort_values(["year", "month", "carrier", "airport"])

    # Verify integrity
    if (delay_df.empty):
        logger.setLevel(logging.ERROR)
        logger.error("No delay data extracted, ensure data exists")
        raise ValueError("No delay extracted, ensure data exists")
    return delay_df


if __name__ == "__main__":
    print(extract_delay_data().head())
