
import pandas as pd


def merge_main(airport_df: pd.DataFrame,
               delay_df: pd.DataFrame) -> pd.DataFrame:
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
