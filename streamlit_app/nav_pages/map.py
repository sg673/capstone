import pandas as pd
import streamlit as st
import plotly.express as px  # type: ignore
from util import STATE_NAMES


def map_display(data: pd.DataFrame):

    ct_cols = [col for col in data.columns if col.endswith('_ct')]
    agg_dict = {'lat': 'mean', 'lon': 'mean', 'arr_flights': 'sum'}
    agg_dict.update({col: 'sum' for col in ct_cols})

    state_summary = data.groupby(['state', 'year']).agg(agg_dict).reset_index()
    state_summary['total_ct'] = state_summary[ct_cols].sum(axis=1)
    state_summary['arr_flights_pct'] = round(
        (state_summary['total_ct'] / state_summary['arr_flights']) * 100, 2)
    state_summary['state_name'] = state_summary['state'].map(STATE_NAMES)

    for col in ct_cols:
        pct_col = col.replace('_ct', '_pct_of_delays')
        state_summary[pct_col] = round(
            (state_summary[col] / state_summary['total_ct']) * 100, 2)

    with st.container(key="us-map"):
        cols = st.columns(10)

        with cols[0]:
            selected_year = st.selectbox("Selected Year",
                                         sorted(state_summary['year']
                                                .unique()))

        with cols[1]:
            delay_options = ['All Delays'] + [col.replace("_ct", "").title()
                                              for col in ct_cols]
            selected_delay = st.selectbox("Delay Type", delay_options)

        filtered_data = state_summary[state_summary['year'] == selected_year]

        if selected_delay == 'All Delays':
            color_col = "arr_flights_pct"
            title_delay = "All Late Arrivals"
        else:
            color_col = f"{selected_delay.lower()}_pct_of_delays"
            title_delay = f"{selected_delay} Delays"

        fig = px.choropleth(
            filtered_data,
            locations='state',
            color=color_col,
            locationmode='USA-states',
            scope='usa',
            title=f'{title_delay} Percentage by State - {selected_year}',
            labels={color_col: f'{title_delay} Percentage (%)'},
            range_color=[state_summary[color_col].min(),
                         state_summary[color_col].max()],
            hover_name='state_name',
            color_continuous_scale="dense"
        )
        fig.update_geos(projection_type="albers usa")
        fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            height=600,
            paper_bgcolor='rgba(0,0,0,0)',
            geo_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, height=800, on_select="ignore")
