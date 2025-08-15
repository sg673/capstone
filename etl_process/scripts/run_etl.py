import os
import sys
from config.env_config import setup_env
from src.extract.extract import extract_main
from src.utils.logging_utils import setup_logger

# Use LOG_BASE_PATH if set (for testing), otherwise use default
log_base_path = os.getenv("LOG_BASE_PATH")
logger = setup_logger(
    "etl_pipeline", "etl_pipeline.log", base_path=log_base_path
)


def main():
    # Get the argument from the run_etl command and set up the environment
    setup_env(sys.argv)
    logger.info(
        f"ETL pipeline started successfully in "
        f"{os.getenv('ENV', 'error')} environment!"
    )

    logger.info("Started Extraction Phase")
    extracted_data = extract_main()
    logger.info("Extraction Phase Completed")


if __name__ == "__main__":
    main()
