import pytest
import pandas as pd
from unittest.mock import patch
from src.transform.transformer import Transformer


# All mock / sample data is AI generated
class TestTransformer:

    @pytest.fixture
    def sample_data(self):
        """Sample DataFrame for testing"""
        return pd.DataFrame({
            'name': ['Airport A', 'Airport B', 'Airport A', 'Airport C'],
            'iata': ['AAA', 'BBB', 'AAA', None],
            'City': ['City A', 'City B', 'City A', 'City C'],
            'Lat': [40.1, 41.2, 40.1, None],
            'Lon': [-74.1, -75.2, -74.1, -76.3],
            'Alt': [100, 200, 100, 300]
        })

    @pytest.fixture
    def airport_config(self):
        """Airport configuration for testing"""
        return {
            'crit_cols': ['name', 'iata'],
            'col_types': {
                'str_cols': ['name', 'iata', 'city'],
                'float_cols': ['lat', 'lon', 'alt'],
                'int_cols': []
            }
        }

    def test_init_valid_config(self, sample_data, airport_config):
        """Test successful initialisation with a valid config"""
        transformer = Transformer(
            sample_data,
            airport_config['crit_cols'],
            airport_config['col_types']
        )
        assert transformer.data.equals(sample_data)
        assert transformer.crit_cols == airport_config['crit_cols']
        assert transformer.col_types == airport_config['col_types']

    def test_init_missing_crit_cols(self, sample_data):
        """Test initialisation with missing critical columns"""
        with pytest.raises(ValueError, match="Critical columns not found"):
            Transformer(
                sample_data,
                ['missing_cols'],
                {'str_cols': [], 'int_cols': [], 'float_cols': []}
            )

    def test_init_missing_col_types(self, sample_data):
        """Test initialisation with missing col_types"""
        with pytest.raises(ValueError, match="Missing required keys"):
            Transformer(
                sample_data,
                ['name'],
                {'str_cols': []}
            )

    def test_remove_duplicates(self, sample_data, airport_config):
        """Test duplicate removal"""
        transformer = Transformer(
            sample_data,
            airport_config['crit_cols'],
            airport_config['col_types']
        )
        transformer.remove_duplicates()
        assert len(transformer.clean_data) == 3
        assert not transformer.clean_data.duplicated().any()

    def test_drop_critical_nulls(self, airport_config):
        """Test rows with critical nulls are dropped"""
        data_with_nulls = pd.DataFrame({
            'name': ['Airport A', None, 'Airport C'],
            'iata': ['AAA', 'BBB', None],
            'city': ['City A', 'City B', 'City C'],
            'lat': [40.1, 41.2, 42.3],
            'lon': [-74.1, -75.2, -76.3],
            'alt': [100, 200, 300]
        })
        transformer = Transformer(
            data_with_nulls,
            airport_config['crit_cols'],
            airport_config['col_types']
        )
        transformer.clean_data = data_with_nulls.copy()
        transformer.handle_nulls()
        assert len(transformer.clean_data) == 1
        assert transformer.clean_data.iloc[0]['name'] == 'Airport A'

    def test_nulls_filled(self, airport_config):
        """Test that non-critical nullsa are filled"""
        data_with_nulls = pd.DataFrame({
            'name': ['Airport A', 'Airport B'],
            'iata': ['AAA', 'BBB'],
            'city': [None, 'City B'],
            'lat': [40.1, None],
            'lon': [-74.1, -75.2],
            'alt': [100, 200]
        })
        transformer = Transformer(
            data_with_nulls,
            airport_config['crit_cols'],
            airport_config['col_types']
        )
        transformer.clean_data = data_with_nulls.copy()
        transformer.handle_nulls()
        assert transformer.clean_data.iloc[0]['city'] == 'N/A'
        assert transformer.clean_data.iloc[1]['lat'] == 0
        assert not transformer.clean_data.isna().any().any()

    def test_format_data_types(self, sample_data, airport_config):
        """Tes data type conversion"""
        transformer = Transformer(
            sample_data,
            airport_config['crit_cols'],
            airport_config['col_types']
        )
        transformer.clean_data = sample_data.copy()
        transformer.clean_data.columns = ['name', 'iata',
                                          'city', 'lat',
                                          'lon', 'alt']
        transformer.format_data_types()
        assert transformer.clean_data['name'].dtype == 'string'
        assert transformer.clean_data['iata'].dtype == 'string'
        assert transformer.clean_data['city'].dtype == 'string'
        assert transformer.clean_data['lat'].dtype == 'float64'
        assert transformer.clean_data['lon'].dtype == 'float64'
        assert transformer.clean_data['alt'].dtype == 'float64'


class TestTransformerDelayData:

    @pytest.fixture
    def delay_data(self):
        """Sample delay DataFrame for testing"""
        return pd.DataFrame({
            'year': [2023, 2023, 2023, 2023],
            'month': [1, 2, 1, 3],
            'carrier': ['AA', 'BB', 'AA', None],
            'carrier_name': ['American', 'Blue', 'American', 'Unknown'],
            'airport': ['JFK', 'LAX', 'JFK', 'ORD'],
            'airport_name': ['JFK Airport', 'LAX Airport',
                             'JFK Airport', None],
            'Arr Flights': [100, 200, 100, 150],
            'Carrier CT': [1.5, 2.0, 1.5, None]
        })

    @pytest.fixture
    def delay_config(self):
        """Delay configuration for testing"""
        return {
            'crit_cols': ['year', 'month',
                          'carrier', 'carrier_name',
                          'airport', 'airport_name'],
            'col_types': {
                'str_cols': ['carrier', 'carrier_name',
                             'airport', 'airport_name'],
                'int_cols': ['year', 'month', 'arr_flights'],
                'float_cols': ['carrier_ct']
            }
        }

    def test_delay_data_cleaning(self, delay_data, delay_config):
        """Test cleaning of delay data"""
        transformer = Transformer(
            delay_data,
            delay_config['crit_cols'],
            delay_config['col_types']
        )
        result = transformer.clean()
        assert len(result) == 2
        assert result['carrier_ct'].fillna(0).equals(result['carrier_ct'])
