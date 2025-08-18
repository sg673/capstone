import pandas as pd
from src.utils.logging_utils import setup_logger
import logging

logger = setup_logger(__name__, "extract_data.log", level=logging.DEBUG)


def merge_main(airport_df: pd.DataFrame,
               delay_df: pd.DataFrame) -> pd.DataFrame:
    """
        Merge airport and delay dataframes and extract state information.

        Args:
            airport_df: DataFrame containing airport
            information with 'iata' codes
            delay_df: DataFrame containing flight
            delay data with 'airport' codes

        Returns:
            Merged DataFrame with state column added and
            unnecessary columns removed
    """
    merged_df = delay_df.merge(airport_df,
                               left_on='airport',
                               right_on='iata',
                               how='left')
    records = len(merged_df)
    # ~5000 unmatched codes
    merged_df.dropna(inplace=True)
    dropped_rows = records - len(merged_df)
    percentage_dropped = round(dropped_rows / records * 100, 2)

    logger.info(f"{dropped_rows} rows unmatched and removed - "
                f"{percentage_dropped}% removed")
    merged_df['state'] = merged_df['airport_name'] \
        .str.split(', ') \
        .str[1].str.split(':').str[0]
    merged_df = merged_df.drop(['arr_del15',
                                'airport_name',
                                'airport'], axis=1)
    return merged_df
