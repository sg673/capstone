import pandas as pd
import streamlit as st


def map_display(data: pd.DataFrame):
    st.title("MAP")

    ct_cols = [col for col in data.columns if col.endswith('_ct')]
    agg_dict = {'lat': 'mean', 'lon': 'mean', 'arr_flights': 'sum'}
    agg_dict.update({col: 'sum' for col in ct_cols})

    state_summary = data.groupby(['state', 'year']).agg(agg_dict).reset_index()
    state_summary['total_ct'] = state_summary[ct_cols].sum(axis=1)
    state_summary['arr_flights_pct'] = round(
        (state_summary['total_ct'] / state_summary['arr_flights']) * 100, 2)
    st.map(data=state_summary)
