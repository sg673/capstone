import pandas as pd
import streamlit as st
import plotly.express as px
from util import STATE_NAMES


def graph_display(data: pd.DataFrame):
    ct_cols = [col for col in data.columns if col.endswith('_ct')]
    delay_cols = ['carrier_delay', 'weather_delay', 'nas_delay', 'security_delay', 'late_aircraft_delay']

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

    agg_dict = {col: 'sum' for col in delay_cols + ct_cols}
    agg_dict['arr_flights'] = 'sum'
    grouped_data = filtered_data.groupby(group_by).agg(agg_dict).reset_index()

    if group_by == 'state':
        grouped_data['state_name'] = grouped_data['state'].map(STATE_NAMES)
        display_col = 'state_name'
    else:
        display_col = group_by

    grouped_data['total_delays_minutes'] = grouped_data[delay_cols].sum(axis=1)
    grouped_data['total_delays'] = grouped_data[ct_cols].sum(axis=1)

    grouped_data['avg_delay_time'] = (grouped_data['total_delays_minutes']
                                      / grouped_data['total_delays']).round(2)
    


    for col in ct_cols:
        pct_col = col.replace('_ct', '_pct')
        grouped_data[pct_col] = round(
            (grouped_data[col] / grouped_data['arr_flights']) * 100, 2)

    ascending = sort_order == 'Ascending'
    grouped_data = grouped_data.sort_values('avg_delay_time',
                                            ascending=ascending)

    years_str = ', '.join(map(str, selected_years))
    fig = px.bar(
        grouped_data.head(20),
        x=group_by,
        y='avg_delay_time',
        color='avg_delay_time',
        title=f'Average Delay Time by {selected_group.title()} - '
        f'{years_str}',
        labels={'avg_delay_time': 'Average Delay Time (minutes)'},
        hover_name=display_col,
        color_continuous_scale="dense"
    )

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')

    st.plotly_chart(fig, use_container_width=True)


def map_display(data: pd.DataFrame):
    ct_cols = [col for col in data.columns if col.endswith('_ct')]
    agg_dict = {'lat': 'mean', 'lon': 'mean', 'arr_flights': 'sum',
                'arr_flights_pct': 'mean'}
    agg_dict.update({col: 'sum' for col in ct_cols})

    state_summary = data.groupby(['state', 'year']).agg(agg_dict).reset_index()
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
            selected_delay = st.selectbox("Delay Type", delay_options[:-2])

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
            height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            geo_bgcolor='rgba(0,0,0,0)'
        )

        st.plotly_chart(fig, height=400, on_select="ignore")


def pres_visual():

    # Load data
    try:
        data = pd.read_csv("../etl_process/data/output/merged_data.csv",encoding="latin-1",index_col=0)
    except FileNotFoundError:
        st.error("Data file not found. Please run the ETL process first.")
        return

    # Visualization type selector
    viz_type = st.selectbox("Select Visualization Type:", 
                           ["Graph View", "Map View"])

    st.markdown("---")

    if viz_type == "Graph View":
        graph_display(data)

    elif viz_type == "Map View":
        map_display(data)