from pathlib import Path
import logging
from typing import Tuple


def _ensure_log_directory(base_path=None):
    """Ensure the logs directory exists."""
    project_root = Path(base_path or __file__).resolve().parent.parent
    log_directory = project_root / "logs"
    log_directory.mkdir(parents=True, exist_ok=True)
    return log_directory


def _create_formatter():
    """Create a standard log formatter."""
    return logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def _create_handlers(log_directory, log_file, level):
    """Create file and console handlers."""
    file_handler = logging.FileHandler(log_directory / log_file)
    file_handler.setLevel(level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)

    formatter = _create_formatter()
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    return file_handler, console_handler


def setup_logger(name, log_file, level=logging.DEBUG, base_path=None):
    """Function to setup a logger; can be used in multiple modules."""
    log_directory = _ensure_log_directory(base_path)

    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        file_handler, console_handler = _create_handlers(
            log_directory, log_file, level
        )
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger


# Function stolen from eds code

def log_extract_success(
    logger: logging.Logger,
    type: str,
    shape: Tuple[int, int],
    execution_time: float,
    expected_rate: float
) -> None:
    logger.setLevel(logging.INFO)
    logger.info(f"Data extraction successful for {type}!")
    logger.info(f"Extracted {shape[0]} rows " f"and {shape[1]} columns")
    logger.info(f"Execution time: {execution_time} seconds")

    if execution_time / shape[0] <= expected_rate:
        logger.info(
            "Execution time per row: " f"{execution_time / shape[0]} seconds"
        )
    else:
        logger.setLevel(logging.WARNING)
        logger.warning(
            f"Execution time per row exceeds {expected_rate}: "
            f"{execution_time / shape[0]} seconds"
        )
