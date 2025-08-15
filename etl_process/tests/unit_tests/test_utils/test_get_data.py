import pytest
import pandas as pd
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.utils.get_data import get_raw_file


class TestGetRawFile:

    @patch('src.utils.get_data.pd.read_csv')
    def test_get_raw_file_success(self, mock_read_csv):
        """Test successful file reading"""
        mock_df = pd.DataFrame({'col1': [1, 2], 'col2': ['a', 'b']})
        mock_read_csv.return_value = mock_df
        
        result = get_raw_file("test.csv")
        
        assert result.equals(mock_df)
        mock_read_csv.assert_called_once()

    @patch('src.utils.get_data.pd.read_csv')
    def test_get_raw_file_not_found(self, mock_read_csv):
        """Test FileNotFoundError handling"""
        mock_read_csv.side_effect = FileNotFoundError("File not found")
        
        with pytest.raises(FileNotFoundError, match="File test.csv not found"):
            get_raw_file("test.csv")

    @patch('src.utils.get_data.pd.read_csv')
    def test_get_raw_file_general_exception(self, mock_read_csv):
        """Test general exception handling"""
        mock_read_csv.side_effect = Exception("Read error")
        
        with pytest.raises(Exception, match="Error reading file test.csv"):
            get_raw_file("test.csv")
