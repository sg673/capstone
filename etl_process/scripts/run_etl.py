import os
import sys
import time
from config.env_config import setup_env
from src.load.load import load_main
from src.extract.extract import extract_main
from src.transform.transform import transform_main
from src.utils.logging_utils import setup_logger

# Use LOG_BASE_PATH if set (for testing), otherwise use default
log_base_path = os.getenv("LOG_BASE_PATH")
logger = setup_logger(
    "etl_pipeline", "etl_pipeline.log", base_path=log_base_path
)


def main():
    start_time = time.time()
    # Get the argument from the run_etl command and set up the environment
    setup_env(sys.argv)
    logger.info(
        f"ETL pipeline started successfully in "
        f"{os.getenv('ENV', 'error')} environment!"
    )
    post_data = None

    # Determines wether or not to save each step to a file
    try:
        post_data = os.getenv("POST_DATA", False)
        if post_data == "True":
            post_data = True
        else:
            post_data = False
    except KeyError:
        post_data = False

    logger.info("Started Extraction Phase")
    extract_start = time.time()
    extracted_data = extract_main(post_data)
    extract_time = time.time() - extract_start
    logger.info(f"Extraction Phase Completed in {extract_time:.2f} seconds")

    logger.info("Started Transform Phase")
    transform_start = time.time()
    transformed_data = transform_main(extracted_data, post_data)
    transform_time = time.time() - transform_start
    logger.info(f"Transform Phase Completed in {transform_time:.2f} seconds")

    logger.info("Starting Load Phase")
    load_start = time.time()
    load_main(transformed_data)
    load_time = time.time() - load_start
    logger.info(f"Load Phase Completed in {load_time:.2f} seconds")

    total_time = time.time() - start_time
    logger.info(f"ETL Pipeline completed in {total_time:.2f} seconds total")
if __name__ == "__main__":
    main()
