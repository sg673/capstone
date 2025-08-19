import pytest
import pandas as pd
from unittest.mock import Mock, patch, mock_open
from sqlalchemy import Engine
from src.load.load_database import load_to_database, execute_sql


class TestLoadDatabase:

    @pytest.fixture
    def sample_data(self):
        return pd.DataFrame({
            "name": ["test1", "test2"],
            "age": [25, 30]
        })

    @pytest.fixture
    def mock_engine(self):
        return Mock(spec=Engine)

    @patch('src.load.load_database.load_db_config')
    @patch('src.load.load_database.create_engine')
    @patch('src.load.load_database.execute_sql')
    @patch('pandas.DataFrame.to_sql')
    def test_load_to_database_success(self,
                                      mock_to_sql,
                                      mock_execute_sql,
                                      mock_create_engine,
                                      mock_config,
                                      sample_data,
                                      mock_engine):
        mock_config.return_value = {
            "target_database": {
                "user": "test", "password": "test",
                "host": "test", "port": "5432", "dbname": "test"
            }
        }
        mock_create_engine.return_value = mock_engine
        mock_execute_sql.return_value = True
        result = load_to_database(sample_data)
        assert result is True
        mock_to_sql.assert_called_once()
        assert mock_execute_sql.call_count == 2

    @patch('src.load.load_database.load_db_config')
    def test_load_to_database_config_error(self, mock_config, sample_data):
        mock_config.side_effect = Exception("config error")

        result = load_to_database(sample_data)
        assert result is False

    @patch('builtins.open', new_callable=mock_open, read_data="SELECT COUNT(*) as result")
    @patch('src.load.load_database.pd.read_sql_query')
    def test_sql_success(self, mock_read_sql, mock_file, mock_engine):
        mock_read_sql.return_value = pd.DataFrame({"result": [5]})

        with patch("pathlib.Path.exists", return_value=True):
            result = execute_sql(mock_engine, "test_query", 5)
        assert result is True

    def test_sql_file_not_found(self, mock_engine):
        with patch("pathlib.Path.exists", return_value=False):
            result = execute_sql(mock_engine, "nonthere", 5)
        assert result is False

    @patch('builtins.open', new_callable=mock_open, read_data="SELECT COUNT(*) as result")
    @patch('src.load.load_database.pd.read_sql_query')
    def test_sql_mismatch(self, mock_read_sql, mock_file, mock_engine):
        mock_read_sql.return_value = pd.DataFrame({"result": [3]})

        with patch("pathlib.Path.exists", return_value=True):
            result = execute_sql(mock_engine, "test_query", 5)
        assert result is False
