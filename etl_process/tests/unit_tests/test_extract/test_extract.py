import pytest
from unittest.mock import patch, MagicMock
from src.extract.extract import extract_main


class TestExtractMain:

    @patch('src.extract.extract.extract_airport_locations')
    def test_extract_main_calls_airport_extraction(self, mock_extract_airports):
        """Test that extract_main calls the airport extraction function"""
        extract_main()
        mock_extract_airports.assert_called_once()

    @patch('src.extract.extract.extract_airport_locations')
    def test_extract_main_handles_extraction_error(self, mock_extract_airports):
        """Test that extract_main propagates extraction errors"""
        mock_extract_airports.side_effect = Exception("Extraction failed")

        with pytest.raises(Exception, match="Extraction failed"):
            extract_main()
