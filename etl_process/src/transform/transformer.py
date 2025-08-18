import pandas as pd
from src.utils.logging_utils import setup_logger
import logging

logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)


class Transformer:
    def __init__(self, data: pd.DataFrame,
                 crit_cols: "list[str]",
                 col_types: "dict[str,list[str]]"):
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
        self.remove_duplicates()
        self.format_columns()
        self.handle_nulls()
        self.format_data_types()
        pass

    def remove_duplicates(self):
        duplicated_rows = self.data.duplicated()
        self.clean_data = self.data[~duplicated_rows]
        logger.info(f"Removed {duplicated_rows.sum()} duplicate rows")

    def format_columns(self):
        self.clean_data.columns = self.clean_data \
                                  .columns.str \
                                  .lower().str.replace(" ", "_")
        logger.info("Column names formatted")

    def handle_nulls(self):
        rows_before_drop = len(self.clean_data)
        self.clean_data = self.clean_data.dropna(subset=self.crit_cols)
        rows_dropped = rows_before_drop - len(self.clean_data)

        rows_with_nulls = self.clean_data.isna().any(axis=1).sum()
        nulls_before_fill = self.clean_data.isna().sum().sum()
        self.clean_data = self.clean_data.fillna(0)
        nulls_after_fill = self.clean_data.isna().sum().sum()

        if nulls_after_fill == 0:
            logger.info(f"Dropped {rows_dropped} rows with critical nulls, "
                        f"filled "
                        f"{nulls_before_fill} nulls in {rows_with_nulls} rows")
        else:
            logger.warning(f"could not handle {nulls_after_fill} nulls")

    def format_data_types(self):
        type_mapping = {
            "str_cols": "string",
            "int_cols": "int64",
            "float_cols": "float64"
        }

        for col_key, dtype in type_mapping.items():
            cols = self.col_types[col_key]
            self.clean_data[cols] = self.clean_data[cols].astype(dtype)
