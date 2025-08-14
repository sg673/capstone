from src.utils.get_data import get_raw_file
import pandas as pd


def extract_airport_locations() -> pd.DataFrame:
    """
        Extracts and processes airport location data for US airports from a
        CSV file. This function reads the 'airports.csv' file using the
        `get_raw_file` utility, filters the data to include only airports
        located in the United States, sorts the results by the IATA code,
        selects relevant columns, and replaces any occurrences of the string
        '\\N' with None to standardize missing values.
        Returns:
            pd.DataFrame: A DataFrame containing the following columns for
            US airports:
                - id: Airport identifier
                - name: Name of the airport
                - city: City where the airport is located
                - iata: IATA airport code
                - lat: Latitude of the airport
                - lon: Longitude of the airport
                - alt: Altitude of the airport
        Raises:
            FileNotFoundError: If the 'airports.csv' file does not exist.
            KeyError: If expected columns are missing from the CSV file.
    """
    EXPECTED_SCHEMA = ["id", "name", "city",
                       "country", "iata", "icao",
                       "lat", "lon", "alt", "tz",
                       "dst", "timezone", "type", "source"]

    airports_df = get_raw_file("airports.csv")

    # Validate schema
    missing_columns = set(EXPECTED_SCHEMA) - set(airports_df.columns)
    if missing_columns:
        raise KeyError(f"Missing expected columns: {missing_columns}")

    # Filter American airports
    us_airports_df = (airports_df[airports_df['country'] == 'United States']
                      .sort_values(by="iata"))

    # Remove Uncessesary columns
    us_airports_df = us_airports_df[['id', 'name', 'city', 'iata', 'lat',
                                     'lon', 'alt']]

    # Replace all \N with None so pandas recognises them as nulls
    us_airports_df = us_airports_df.replace('\\N', None)

    return us_airports_df


if __name__ == "__main__":
    print(extract_airport_locations().head())
