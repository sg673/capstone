
import pandas as pd


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
    # ~5000 unmatched codes
    merged_df.dropna(inplace=True)
    merged_df['state'] = merged_df['airport_name'] \
        .str.split(', ') \
        .str[1].str.split(':').str[0]
    merged_df = merged_df.drop(['arr_del15',
                                'airport_name',
                                'airport'], axis=1)
    return merged_df
