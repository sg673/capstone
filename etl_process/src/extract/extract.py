from src.extract.get_delay_data import extract_delay_data
from src.extract.get_airports import extract_airport_locations


def extract_main() -> None:
    """
        Runs the extraction phase
    """
    extract_airport_locations()
    extract_delay_data()
