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

