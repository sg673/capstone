import pandas as pd
import streamlit as st
import plotly.express as px

# AI generated
state_names = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas',
    'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut',
    'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii',
    'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa',
    'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine',
    'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan',
    'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri',
    'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada',
    'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
    'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota',
    'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania',
    'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota',
    'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia',
    'WI': 'Wisconsin', 'WY': 'Wyoming'
}


def map_display(data: pd.DataFrame):

    ct_cols = [col for col in data.columns if col.endswith('_ct')]
    agg_dict = {'lat': 'mean', 'lon': 'mean', 'arr_flights': 'sum'}
    agg_dict.update({col: 'sum' for col in ct_cols})

    state_summary = data.groupby(['state', 'year']).agg(agg_dict).reset_index()
    state_summary['total_ct'] = state_summary[ct_cols].sum(axis=1)
    state_summary['arr_flights_pct'] = round(
        (state_summary['total_ct'] / state_summary['arr_flights']) * 100, 2)
    state_summary['state_name'] = state_summary['state'].map(state_names)

    with st.container(key="us-map"):
        cols = st.columns(10)
        with cols[0]:
            st.write("Selected Year")
        with cols[1]:
            selected_year = st.selectbox("Selected Year",
                                         sorted(state_summary['year']
                                                .unique()),
                                         label_visibility="collapsed")
            filtered_data = state_summary[
                state_summary['year'] == selected_year]

        fig = px.choropleth(
            filtered_data,
            locations='state',
            color='arr_flights_pct',
            locationmode='USA-states',
            scope='usa',
            title=f'Flight Arrival Percentage by State - {selected_year}',
            labels={'arr_flights_pct': 'Late Arrival Percentage (%)'},
            range_color=[state_summary['arr_flights_pct'].min(),
                         state_summary['arr_flights_pct'].max()],
            hover_name='state_name'
        )
        fig.update_geos(projection_type="albers usa")
        fig.update_layout(
            margin=dict(l=20, r=20, t=20, b=20),
            paper_bgcolor="#cfe0e8",
            height=600
        )

        st.plotly_chart(fig, height=800, on_select="ignore")
