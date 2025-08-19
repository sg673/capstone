import pandas as pd
from src.load.load_database import load_to_database
from src.utils.logging_utils import setup_logger
import logging

logger = setup_logger(__name__, "load_data.log", level=logging.DEBUG)


def load_main(data: pd.DataFrame):

    logger.info("Started load to database")
    load_to_database(data)
