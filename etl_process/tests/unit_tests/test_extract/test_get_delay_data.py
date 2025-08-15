import pytest
import pandas as pd
from unittest.mock import patch
from src.extract.get_delay_data import extract_delay_data


# All mock data is AI generated
class TestExtractDelayData:

    @patch('src.extract.get_delay_data.get_raw_file')
    def test_extract_delay_data_success(self, mock_get_raw_file):
        """Test successful extraction of delay data"""
        mock_data = pd.DataFrame({
            'year': [2023, 2023, 2023],
            'month': [1, 1, 2],
            'carrier': ['AA', 'DL', 'UA'],
            'carrier_name': [
                'American Airlines',
                'Delta Air Lines',
                'United Airlines'
                ],
            'airport': ['ATL', 'LAX', 'ORD'],
            'airport_name': ['Atlanta', 'Los Angeles', 'Chicago'],
            'arr_flights': [1000, 800, 1200],
            'arr_del15': [150, 120, 180],
            'carrier_ct': [50, 40, 60],
            'weather_ct': [30, 25, 35],
            'nas_ct': [40, 30, 50],
            'security_ct': [5, 3, 8],
            'late_aircraft_ct': [25, 22, 27],
            'arr_cancelled': [10, 8, 12],
            'arr_diverted': [5, 3, 7],
            'arr_delay': [12000, 9600, 14400],
            'carrier_delay': [4000, 3200, 4800],
            'weather_delay': [2400, 2000, 2800],
            'nas_delay': [3200, 2400, 4000],
            'security_delay': [400, 240, 640],
            'late_aircraft_delay': [2000, 1760, 2160]
        })
        mock_get_raw_file.return_value = mock_data

        result = extract_delay_data()

        assert len(result) == 3
        assert all(col in result.columns for col in mock_data.columns)

    @patch('src.extract.get_delay_data.get_raw_file')
    def test_missing_columns_raises_error(self, mock_get_raw_file):
        """Test that missing columns raise KeyError"""
        mock_data = pd.DataFrame({'year': [2023], 'month': [1]})
        mock_get_raw_file.return_value = mock_data

        with pytest.raises(KeyError, match="Missing expected columns"):
            extract_delay_data()

    @patch('src.extract.get_delay_data.get_raw_file')
    def test_empty_data_raises_error(self, mock_get_raw_file):
        """Test that empty data raises ValueError"""

        mock_data = pd.DataFrame({
            'year': [],
            'month': [],
            'carrier': [],
            'carrier_name': [],
            'airport': [],
            'airport_name': [],
            'arr_flights': [],
            'arr_del15': [],
            'carrier_ct': [],
            'weather_ct': [],
            'nas_ct': [],
            'security_ct': [],
            'late_aircraft_ct': [],
            'arr_cancelled': [],
            'arr_diverted': [],
            'arr_delay': [],
            'carrier_delay': [],
            'weather_delay': [],
            'nas_delay': [],
            'security_delay': [],
            'late_aircraft_delay': []
        })
        mock_get_raw_file.return_value = mock_data

        with pytest.raises(ValueError, match="No delay extracted"):
            extract_delay_data()

    @patch('src.extract.get_delay_data.get_raw_file')
    def test_data_sorting(self, mock_get_raw_file):
        """Test that data is sorted correctly"""
        mock_data = pd.DataFrame({
            'year': [2023, 2022, 2023],
            'month': [2, 12, 1],
            'carrier': ['UA', 'AA', 'DL'],
            'carrier_name': ['United', 'American', 'Delta'],
            'airport': ['ORD', 'ATL', 'LAX'],
            'airport_name': ['Chicago', 'Atlanta', 'Los Angeles'],
            'arr_flights': [1200, 1000, 800],
            'arr_del15': [180, 150, 120],
            'carrier_ct': [60, 50, 40],
            'weather_ct': [35, 30, 25],
            'nas_ct': [50, 40, 30],
            'security_ct': [8, 5, 3],
            'late_aircraft_ct': [27, 25, 22],
            'arr_cancelled': [12, 10, 8],
            'arr_diverted': [7, 5, 3],
            'arr_delay': [14400, 12000, 9600],
            'carrier_delay': [4800, 4000, 3200],
            'weather_delay': [2800, 2400, 2000],
            'nas_delay': [4000, 3200, 2400],
            'security_delay': [640, 400, 240],
            'late_aircraft_delay': [2160, 2000, 1760]
        })
        mock_get_raw_file.return_value = mock_data

        result = extract_delay_data()

        # Check sorting: 2022-12 should come first, then 2023-01, then 2023-02
        assert result.iloc[0]['year'] == 2022
        assert result.iloc[1]['year'] == 2023 and result.iloc[1]['month'] == 1
        assert result.iloc[2]['year'] == 2023 and result.iloc[2]['month'] == 2
