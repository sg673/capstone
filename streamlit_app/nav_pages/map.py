import pandas as pd
import streamlit as st
import plotly.express as px


def map_display(data: pd.DataFrame):
    st.title("MAP")

    ct_cols = [col for col in data.columns if col.endswith('_ct')]
    agg_dict = {'lat': 'mean', 'lon': 'mean', 'arr_flights': 'sum'}
    agg_dict.update({col: 'sum' for col in ct_cols})

    state_summary = data.groupby(['state', 'year']).agg(agg_dict).reset_index()
    state_summary['total_ct'] = state_summary[ct_cols].sum(axis=1)
    state_summary['arr_flights_pct'] = round(
        (state_summary['total_ct'] / state_summary['arr_flights']) * 100, 2)

    fig = px.choropleth(
        state_summary,
        locations='state',
        color='arr_flights_pct',
        locationmode='USA-states',
        scope='usa',
        title='Flight Arrival Percentage by State'
    )
    fig.update_geos(projection_type="albers usa")
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        paper_bgcolor="#cfe0e8",
        height=800
    )
    with st.container(key="us-map"):
        st.plotly_chart(fig, height=800, on_select="ignore")
