

from pathlib import Path
import pandas as pd
from sqlalchemy import Engine, create_engine
from config.db_config import load_db_config
from src.utils.logging_utils import setup_logger
import logging

logger = setup_logger(__name__, "load_data.log", level=logging.DEBUG)


def load_to_database(data: pd.DataFrame) -> bool:
    """
    Load DataFrame to PostgreSQL database.

    Args:
        data: DataFrame to load

    Returns:
        bool: True if successful, False otherwise
    """
    try:
        config = load_db_config()
        db_config = config["target_database"]

        engine = create_engine(
            f"postgresql://{db_config['user']}:{db_config['password']}@"
            f"{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
        )

        subset = data.head(10000)  # limit upload to 10000 records
        subset.to_sql("sam_capstone",
                      engine,
                      index=False,
                      schema="de_2506_a",
                      if_exists="replace")
        logger.info(f"Loaded {len(subset)} rows to database")

        # validate database shape
        return execute_sql(engine, "count_records", len(subset)) and \
            execute_sql(engine, "count_columns", len(subset.columns))

    except Exception as e:
        logger.error(f"Database loading failed - {e}")
        return False


def execute_sql(engine: Engine, file_name: str, expected_result) -> bool:
    """
    Execute SQL query from file and validate result against expected value.

    Args:
        engine: SQLAlchemy database engine
        file_name: Name of SQL file (without .sql extension) in src/sql directory
        expected_result: Expected query result value for validation

    Returns:
        bool: True if query result matches expected value, False otherwise
    """

    current_dir = Path(__file__).parent
    sql_file = current_dir.parent / "sql" / f"{file_name}.sql"
    if not sql_file.exists():
        logger.error(f"Sql file {file_name} not found")
        return False
    with open(sql_file, "r") as query_file:
        query = query_file.read()
    output = pd.read_sql_query(query, engine).iloc[0]['result']

    if output != expected_result:
        logger.error(f"Expected: {expected_result},"
                     f"Got: {output}")
        return False
    return True


if __name__ == "__main__":
    test1 = pd.DataFrame({
        "name": ["test1", "test2"],
        "address": ["1 example", "2 example"],
        "age": [14, 26]
    })
    load_to_database(test1)
