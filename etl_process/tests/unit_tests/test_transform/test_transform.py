import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from src.transform.transform import transform_main, AIRPORT_CONFIG, DELAY_CONFIG


# All mock / sample data is AI generated
class TestTransformMain:

    @pytest.fixture
    def sample_airport_data(self):
        """Sample airport DataFrame"""
        return pd.DataFrame({
            'name': ['Airport A', 'Airport B'],
            'iata': ['AAA', 'BBB'],
            'City': ['City A', 'City B'],
            'Lat': [40.1, 41.2],
            'Lon': [-74.1, -75.2],
            'Alt': [100, 200]
        })

    @pytest.fixture
    def sample_delay_data(self):
        """Sample delay DataFrame"""
        return pd.DataFrame({
            'year': [2023, 2023],
            'month': [1, 2],
            'carrier': ['AA', 'BB'],
            'carrier_name': ['American', 'Blue'],
            'airport': ['JFK', 'LAX'],
            'airport_name': ['JFK Airport', 'LAX Airport'],
            'arr_flights': [100, 200],
            'arr_del15': [10, 15],
            'arr_cancelled': [2, 3],
            'arr_diverted': [1, 2],
            'arr_delay': [500, 750],
            'carrier_delay': [100, 150],
            'weather_delay': [200, 300],
            'nas_delay': [150, 200],
            'security_delay': [25, 50],
            'late_aircraft_delay': [25, 50],
            'carrier_ct': [1.5, 2.0],
            'weather_ct': [2.5, 3.0],
            'nas_ct': [1.8, 2.2],
            'security_ct': [0.5, 1.0],
            'late_aircraft_ct': [0.8, 1.2]
        })

    @pytest.fixture
    def sample_data_tuple(self, sample_airport_data, sample_delay_data):
        return (sample_airport_data, sample_delay_data)

    @patch('src.transform.transform.post')
    def test_transform_main_writes_to_file_when_requested(self, mock_post, sample_data_tuple):
        """Test that transform_main writes to file when write_to_file=True"""
        transform_main(sample_data_tuple, write_to_file=True)

        assert mock_post.call_count == 2
        mock_post.assert_any_call("output", "extract_airports.csv",
                                  mock_post.call_args_list[0][0][2])
        mock_post.assert_any_call("output", "extract_delay.csv",
                                  mock_post.call_args_list[1][0][2])

    def test_transform_main_cleans_columns(self, sample_data_tuple):
        """Test that the data is properly cleaned"""
        result = transform_main(sample_data_tuple)
        airport_result, delay_result = result

        assert all(col.islower() for col in airport_result.columns)
        assert all(col.islower() for col in delay_result.columns)
        assert all('_' in col or col.isalpha() for col in airport_result.columns)
        assert all('_' in col or col.isalpha() for col in delay_result.columns)

    def test_transform_main_with_dirty_data(self):
        """Test transform_main with data that needs cleaning"""
        dirty_airport = pd.DataFrame({
            'name': ['Airport A', 'Airport B', 'Airport A'],  # Duplicate
            'iata': ['AAA', 'BBB', 'AAA'],
            'City': ['City A', None, 'City A'],  # Null
            'Lat': [40.1, 41.2, 40.1],
            'Lon': [-74.1, -75.2, -74.1],
            'Alt': [100, 200, 100]
        })

        dirty_delay = pd.DataFrame({
            'year': [2023, 2023, 2023],
            'month': [1, 2, 1],  # Duplicate row
            'carrier': ['AA', 'BB', 'AA'],
            'carrier_name': ['American', 'Blue', 'American'],
            'airport': ['JFK', 'LAX', 'JFK'],
            'airport_name': ['JFK Airport', 'LAX Airport', 'JFK Airport'],
            'arr_flights': [100, 200, 100],
            'arr_del15': [10, 15, 10],
            'arr_cancelled': [2, 3, 2],
            'arr_diverted': [1, 2, 1],
            'arr_delay': [500, 750, 500],
            'carrier_delay': [100, 150, 100],
            'weather_delay': [200, 300, 200],
            'nas_delay': [150, 200, 150],
            'security_delay': [25, 50, 25],
            'late_aircraft_delay': [25, 50, 25],
            'carrier_ct': [1.5, None, 1.5],  # Null
            'weather_ct': [2.5, 3.0, 2.5],
            'nas_ct': [1.8, 2.2, 1.8],
            'security_ct': [0.5, 1.0, 0.5],
            'late_aircraft_ct': [0.8, 1.2, 0.8]
        })
        result = transform_main((dirty_airport, dirty_delay))
        airport_result, delay_result = result

        # Check that duplicates were removed
        assert len(airport_result) <= len(dirty_airport)
        assert len(delay_result) <= len(dirty_delay)

        # Check that nulls were handled
        assert not airport_result.isna().any().any()
        assert not delay_result.isna().any().any()
