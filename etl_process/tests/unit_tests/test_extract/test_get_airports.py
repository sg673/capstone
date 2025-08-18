import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.extract.get_airports import extract_airport_locations


# All mock data is AI generated
class TestExtractAirportLocations:

    @patch('src.extract.get_airports.get_raw_file')
    def test_extract_airport_locations_success(self, mock_get_raw_file):
        """Test successful extraction of US airports"""
        mock_data = pd.DataFrame({
            'id': [1, 2, 3],
            'name': ['Airport A', 'Airport B', 'Airport C'],
            'city': ['City A', 'City B', 'City C'],
            'country': ['United States', 'United States', 'Canada'],
            'iata': ['AAA', 'BBB', 'CCC'],
            'icao': ['AAAA', 'BBBB', 'CCCC'],
            'lat': [40.0, 41.0, 42.0],
            'lon': [-74.0, -75.0, -76.0],
            'alt': [100, 200, 300],
            'tz': ['EST', 'EST', 'EST'],
            'dst': ['A', 'A', 'A'],
            'timezone': ['America/New_York', 'America/New_York', 'America/Toronto'],
            'type': ['airport', 'airport', 'airport'],
            'source': ['OurAirports', 'OurAirports', 'OurAirports']
        })
        mock_get_raw_file.return_value = mock_data

        result = extract_airport_locations()

        assert len(result) == 2
        assert list(result.columns) == ['name', 'city', 'iata', 'lat', 'lon', 'alt']
        assert all(result['iata'].isin(['AAA', 'BBB']))

    @patch('src.extract.get_airports.get_raw_file')
    def test_missing_columns_raises_error(self, mock_get_raw_file):
        """Test that missing columns raise KeyError"""
        mock_data = pd.DataFrame({'id': [1], 'name': ['Airport']})
        mock_get_raw_file.return_value = mock_data

        with pytest.raises(KeyError, match="Missing expected columns"):
            extract_airport_locations()

    @patch('src.extract.get_airports.get_raw_file')
    def test_no_us_airports_raises_error(self, mock_get_raw_file):
        """Test that no US airports raises ValueError"""
        mock_data = pd.DataFrame({
            'id': [1], 'name': ['Airport'], 'city': ['City'], 'country': ['Canada'],
            'iata': ['AAA'], 'icao': ['AAAA'], 'lat': [40.0], 'lon': [-74.0],
            'alt': [100], 'tz': ['EST'], 'dst': ['A'], 'timezone': ['America/Toronto'],
            'type': ['airport'], 'source': ['OurAirports']
        })
        mock_get_raw_file.return_value = mock_data

        with pytest.raises(ValueError, match="No data extracted"):
            extract_airport_locations()

    @patch('src.extract.get_airports.get_raw_file')
    def test_replaces_null_values(self, mock_get_raw_file):
        """Test that \\N values are replaced with None"""
        mock_data = pd.DataFrame({
            'id': [1], 'name': ['Airport'], 'city': ['\\N'], 'country': ['United States'],
            'iata': ['AAA'], 'icao': ['AAAA'], 'lat': [40.0], 'lon': [-74.0],
            'alt': ['\\N'], 'tz': ['EST'], 'dst': ['A'], 'timezone': ['America/New_York'],
            'type': ['airport'], 'source': ['OurAirports']
        })
        mock_get_raw_file.return_value = mock_data

        result = extract_airport_locations()

        assert result['city'].isna().iloc[0]
        assert result['alt'].isna().iloc[0]
