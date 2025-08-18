import pandas as pd
from src.utils.logging_utils import setup_logger
import logging
from typing import Any

logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)


class Transformer:
    """
        A data transformation class for cleaning and
        formatting pandas DataFrames.

        This class provides methods to clean data by removing duplicates,
        formatting
        column names, handling null values, and converting data types.
    """

    def __init__(self, data: pd.DataFrame,
                 crit_cols: "list[str]",
                 col_types: "dict[str,list[str]]"):
        """Initialize the Transformer with data and configuration.

        Args:
            data: The pandas DataFrame to be transformed
            crit_cols: List of critical column names that cannot
            have null values
            col_types: Dictionary mapping column type categories to
            column lists.
                      Must contain keys: 'str_cols', 'int_cols', 'float_cols'

        Raises:
            ValueError: If critical columns are missing from data or required
                       keys are missing from col_types
        """
        missing_cols = [col for col in crit_cols if col not in data.columns]
        if missing_cols:
            raise ValueError(f"Critical columns not found in data: "
                             f"{missing_cols}")
        required_keys = {"str_cols", "int_cols", "float_cols"}
        missing_keys = required_keys - set(col_types.keys())
        if missing_keys:
            raise ValueError(f"Missing required keys in col_types: "
                             f"{missing_keys}")
        self.data = data
        self.crit_cols = crit_cols
        self.col_types = col_types

    def clean(self):
        """Execute the complete data cleaning pipeline.

        Performs all cleaning operations in sequence: removes duplicates,
        formats columns, converts data types, and handles null values.

        Returns:
            pd.DataFrame: The cleaned DataFrame
        """
        self.remove_duplicates()
        self.format_columns()
        self.format_data_types()
        self.handle_nulls()
        return self.clean_data

    def remove_duplicates(self):
        """Remove duplicate rows from the dataset.

        Creates a clean_data attribute with duplicates removed and logs
        the number of duplicates found.
        """
        duplicated_rows = self.data.duplicated()
        self.clean_data = self.data[~duplicated_rows]
        logger.info(f"Removed {duplicated_rows.sum()} duplicate rows")

    def format_columns(self):
        """Format column names to lowercase with underscores.

        Converts all column names to lowercase and replaces spaces
        with underscores for consistent naming.
        """
        self.clean_data.columns = self.clean_data \
            .columns.str \
            .lower().str.replace(" ", "_")
        logger.info("Column names formatted")

    def handle_nulls(self):
        """Handle null values in the dataset.

        Drops rows with nulls in critical columns, then fills remaining
        nulls with appropriate default values based on column type:
        - String columns: filled with 'N/A'
        - Integer columns: filled with 0
        - Float columns: filled with 0
        """
        rows_before_drop = len(self.clean_data)
        self.clean_data = self.clean_data.dropna(subset=self.crit_cols)
        rows_dropped = rows_before_drop - len(self.clean_data)

        rows_with_nulls = self.clean_data.isna().any(axis=1).sum()
        nulls_before_fill = self.clean_data.isna().sum().sum()

        str_cols = self.col_types["str_cols"]
        int_cols = self.col_types["int_cols"]
        float_cols = self.col_types["float_cols"]

        self.clean_data[str_cols] = self.clean_data[str_cols].fillna("N/A")
        self.clean_data[int_cols] = self.clean_data[int_cols].fillna(0)
        self.clean_data[float_cols] = self.clean_data[float_cols].fillna(0)

        nulls_after_fill = self.clean_data.isna().sum().sum()

        if nulls_after_fill == 0:
            logger.info(f"Dropped {rows_dropped} rows with critical nulls, "
                        f"filled "
                        f"{nulls_before_fill} nulls in {rows_with_nulls} rows")
        else:
            logger.warning(f"could not handle {nulls_after_fill} nulls")

    def format_data_types(self):
        """Convert columns to their specified data types.

        Applies type conversions based on the col_types configuration:
        - str_cols: converted to 'string' dtype
        - int_cols: converted to 'int64' dtype
        - float_cols: converted to 'float64' dtype
        """
        type_mapping: dict[str, Any] = {
            "str_cols": "string",
            "int_cols": "int64",
            "float_cols": "float64"
        }

        for col_key, dtype in type_mapping.items():
            cols = self.col_types[col_key]
            self.clean_data[cols] = self.clean_data[cols].astype(dtype)
        logger.info("columns converted to correct datatypes")
