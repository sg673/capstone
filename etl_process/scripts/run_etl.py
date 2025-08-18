import os
import sys
from config.env_config import setup_env
from src.extract.extract import extract_main
from src.transform.transform import transform_main
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
    extracted_data = extract_main(post_data)
    logger.info("Extraction Phase Completed")

    logger.info("Started Transform Phase")
    transformed_data = transform_main(extracted_data, post_data)
    logger.info("Transform Phase Completed")


if __name__ == "__main__":
    main()
