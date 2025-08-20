import pandas as pd
import streamlit as st
import plotly.express as px
from util import STATE_NAMES


def graph_display(data: pd.DataFrame):
    st.title("GRAPH")

    ct_cols = [col for col in data.columns if col.endswith('_ct')]

    # Filter controls
    col1, col2, col4 = st.columns(3)

    with col1:
        selected_years = st.multiselect("Year", sorted(data['year'].unique()),
                                        default=[data['year'].max()])

    with col2:
        group_options = {
                'Carrier': 'carrier_name',
                'Airport': 'name',
                'State': 'state'
            }
        selected_group = st.selectbox("Group by", list(group_options.keys()))
        group_by = group_options[selected_group]
    with col4:
        sort_order = st.selectbox("Order", ['Descending', 'Ascending'])

    filtered_data = data[data['year'].isin(selected_years)]

    agg_dict = {col: 'sum' for col in ct_cols}
    agg_dict['arr_flights'] = 'sum'
    grouped_data = filtered_data.groupby(group_by).agg(agg_dict).reset_index()

    if group_by == 'state':
        grouped_data['state_name'] = grouped_data['state'].map(STATE_NAMES)
        display_col = 'state_name'
    else:
        display_col = group_by

    grouped_data['total_delays'] = grouped_data[ct_cols].sum(axis=1)
    grouped_data['total_delays_pct'] = round(
        (grouped_data['total_delays'] / grouped_data['arr_flights']) * 100, 2)

    for col in ct_cols:
        pct_col = col.replace('_ct', '_pct')
        grouped_data[pct_col] = round(
            (grouped_data[col] / grouped_data['arr_flights']) * 100, 2)

    ascending = sort_order == 'Ascending'
    grouped_data = grouped_data.sort_values('total_delays_pct',
                                            ascending=ascending)

    years_str = ', '.join(map(str, selected_years))
    fig = px.bar(
        grouped_data.head(20),
        x=group_by,
        y='total_delays_pct',
        color='total_delays_pct',
        title=f'Total Delays Percentage by {selected_group.title()} - {years_str}',
        labels={'total_delays_pct': 'Delay Percentage (%)'},
        hover_name=display_col,
        color_continuous_scale="dense"
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')

    st.plotly_chart(fig, use_container_width=True)
