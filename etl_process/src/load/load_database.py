

from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine
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

        current_dir = Path(__file__).parent
        sql_file_path = current_dir.parent / "sql" / "count_records.sql"
        if not sql_file_path.exists():
            logger.error("Sql file not found")
            return False
        with open(sql_file_path, "r") as query_file:
            query = query_file.read()
        out = pd.read_sql_query(query, engine)
        loaded_records = out.iloc[0]['total']

        if loaded_records != len(subset):
            logger.error(f"Only {loaded_records} records loaded,"
                         f"expected {len(subset)}")
            return False

        return True
    except Exception as e:
        logger.error(f"Database loading failed - {e}")
        return False


if __name__ == "__main__":
    test1 = pd.DataFrame({
        "name": ["test1", "test2"],
        "address": ["1 example", "2 example"],
        "age": [14, 26]
    })
    load_to_database(test1)
