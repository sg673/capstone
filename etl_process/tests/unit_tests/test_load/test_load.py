import pytest
import pandas as pd
from unittest.mock import patch
from src.load.load import load_main


class TestLoad:

    @pytest.fixture
    def sample_data(self):
        return pd.DataFrame({
            "name": ["test1", "test2"],
            "age": [25, 30]
        })

    @patch('src.load.load.load_to_database')
    def test_load_main_success(self,
                               mock_load_to_database,
                               sample_data):
        mock_load_to_database.return_value = True
        load_main(sample_data)
        mock_load_to_database.assert_called_once_with(sample_data)
