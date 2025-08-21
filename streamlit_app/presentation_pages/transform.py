import streamlit as st
import pandas as pd


# The vast majority of this file is AI generated
def show_transformer_methods():
    """Display the actual Transformer class methods"""
    methods = {
        "remove_duplicates()": {
            "description": "Remove duplicate rows from the dataset",
            "code": '''def remove_duplicates(self):
    duplicated_rows = self.data.duplicated()
    self.clean_data = self.data[~duplicated_rows]
    logger.info(f"Removed {duplicated_rows.sum()} duplicate rows")'''
        },
        "format_columns()": {
            "description": "Format column names to lowercase with underscores",
            "code": '''def format_columns(self):
    self.clean_data.columns = self.clean_data \
        .columns.str \
        .lower().str.replace(" ", "_")
    logger.info("Column names formatted")'''
        },
        "handle_nulls()": {
            "description": "Handle null values based on column types and criticality",
            "code": '''def handle_nulls(self):
    # Drop rows with nulls in critical columns
    self.clean_data = self.clean_data.dropna(subset=self.crit_cols)

    # Fill remaining nulls by column type
    str_cols = self.col_types["str_cols"]
    int_cols = self.col_types["int_cols"]
    float_cols = self.col_types["float_cols"]

    self.clean_data[str_cols] = self.clean_data[str_cols].fillna("N/A")
    self.clean_data[int_cols] = self.clean_data[int_cols].fillna(0)
    self.clean_data[float_cols] = self.clean_data[float_cols].fillna(0)'''
        },
        "format_data_types()": {
            "description": "Convert columns to specified data types",
            "code": '''def format_data_types(self):
    type_mapping = {
        "str_cols": "string",
        "int_cols": "int64",
        "float_cols": "float64"
    }

    for col_key, dtype in type_mapping.items():
        cols = self.col_types[col_key]
        self.clean_data[cols] = self.clean_data[cols].astype(dtype)'''
        }
    }
    return methods


def show_merge_function():
    """Display the actual merge function"""
    merge_info = {
        "description": "Merge airport and delay dataframes and "
                       "extract state information",
        "code": '''def merge_main(airport_df: pd.DataFrame, "
                    "delay_df: pd.DataFrame) -> pd.DataFrame:
    # Merge dataframes on airport codes
    merged_df = delay_df.merge(airport_df,
                               left_on='airport',
                               right_on='iata',
                               how='left')

    # Remove unmatched records
    merged_df.dropna(inplace=True)

    # Extract state from airport_name
    merged_df['state'] = merged_df['airport_name'] \
        .str.split(', ') \
        .str[1].str.split(':').str[0]

    # Calculate totals and percentages
    ct_cols = [col for col in merged_df.columns if col.endswith('_ct')]
    merged_df['total_ct'] = merged_df[ct_cols].sum(axis=1)
    merged_df['arr_flights_pct'] = round(
        (merged_df['total_ct'] / merged_df['arr_flights']) * 100, 2)

    # Drop unnecessary columns
    merged_df = merged_df.drop(['arr_del15', 'airport_name', 'airport'],
                               axis=1)

    return merged_df'''
    }
    return merge_info


def simulate_transformer_steps(raw_data):
    """Simulate transformer methods on demo data"""
    # Step 1: Raw data with duplicates and issues
    step1 = raw_data.copy()

    # Step 2: Remove duplicates
    step2 = step1[~step1.duplicated()].copy()

    # Step 3: Format columns
    step3 = step2.copy()
    step3.columns = step3.columns.str.lower().str.replace(" ", "_")
    print(raw_data.head())
    # Step 4: Handle nulls (simulate critical cols)
    step4 = step3.copy()
    crit_cols = ['year', 'month', 'carrier', 'carrier_name',
                 'airport', 'airport_name'] if 'year' in step4.columns \
        else ['name', 'iata']
    step4 = step4.dropna(subset=crit_cols)
    # Fill remaining nulls
    for col in step4.columns:
        if step4[col].dtype == 'object':
            step4[col] = step4[col].fillna('N/A')
        else:
            step4[col] = step4[col].fillna(0)

    # Step 5: Format data types
    step5 = step4.copy()
    for col in step5.columns:
        if col in ['year'] and col in step5.columns:
            step5[col] = step5[col].astype('int64')
        elif step5[col].dtype == 'object':
            step5[col] = step5[col].astype('string')

    return step1, step2, step3, step4, step5


def simulate_merge(delay_df, airport_df):
    """Simulate merge function on demo data"""
    # Prepare airport data with proper format
    airport_clean = airport_df.copy()
    airport_clean = airport_clean.rename(columns={'iata_code': 'iata'})

    # Merge
    merged = delay_df.merge(airport_clean, left_on='airport',
                            right_on='iata', how='left')
    merged = merged.dropna()

    # Extract state
    merged['state'] = merged['airport_name'].str.split(', ') \
        .str[1].str.split(':').str[0]

    # Add demo delay columns for calculation
    if 'carrier_delay' in merged.columns:
        merged['weather_delay_ct'] = merged['carrier_delay'] * 0.5
        merged['nas_delay_ct'] = merged['carrier_delay'] * 0.3
        merged['carrier_delay_ct'] = merged['carrier_delay']

        ct_cols = [col for col in merged.columns if col.endswith('_ct')]
        merged['total_ct'] = merged[ct_cols].sum(axis=1)
        merged['arr_flights'] = 1000  # Demo value
        merged['arr_flights_pct'] = round(
            (merged['total_ct'] / merged['arr_flights']) * 100, 2)

    # Drop unnecessary columns
    drop_cols = ['airport_name', 'airport', 'name', 'city', 'country']
    merged = merged.drop([col for col in drop_cols
                         if col in merged.columns], axis=1)

    return merged


def render_dataframe_step(df, title, step_desc):
    """Render dataframe with transformation info"""
    st.markdown(f"**{title}**")
    st.markdown(step_desc)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Rows", f"{df.shape[0]:,}")
    with col2:
        st.metric("Columns", df.shape[1])
    with col3:
        st.metric("Nulls", df.isnull().sum().sum())

    st.dataframe(df.head(3), use_container_width=True, height=150)


def pres_transform():
    st.markdown("""
    <header>
      <h1>Transformation Phase</h1>
      <h2>Data Cleaning and Validation</h2>
    </header>
    """, unsafe_allow_html=True)

    # Load sample data for demonstration
    try:
        raw_delay = pd.read_csv(
            "../etl_process/data/processed/extract_delay.csv",
            encoding='latin-1', index_col=0)
        raw_airport = pd.read_csv(
            "../etl_process/data/processed/extract_airports.csv",
            encoding='latin-1', index_col=0)
        print(raw_delay.head())
        print(raw_airport.head())
    except:
        # Create sample data if files don't exist
        raw_delay = pd.DataFrame({
            'year': [2020, 2021, 2022, None, 2023],
            'carrier': ['AA', 'DL', 'UA', 'SW', 'AA'],
            'airport': ['JFK', 'LAX', 'ORD', 'DFW', 'JFK'],
            'arr_delay': [15.2, 8.5, None, 12.1, 22.3],
            'carrier_delay': [5.1, 2.3, 4.5, 3.2, 8.1]
        })
        raw_airport = pd.DataFrame({
            'iata_code': ['JFK', 'LAX', 'ORD', None, 'DFW'],
            'name': ['John F Kennedy Intl', 'Los Angeles Intl',
                     'Chicago OHare', 'Missing', 'Dallas Fort Worth'],
            'city': ['New York', 'Los Angeles', 'Chicago', None,
                     'Dallas'],
            'country': ['USA', 'USA', 'USA', 'USA', 'USA'],
            'latitude': [40.6413, 33.9425, 41.9742, None, 32.8998],
            'longitude': [-73.7781, -118.4081, -87.9073, None,
                          -97.0403]
        })

    # Simulate transformation steps
    delay_steps = simulate_transformer_steps(raw_delay)
    airport_steps = simulate_transformer_steps(raw_airport)
    merged_data = simulate_merge(delay_steps[4], airport_steps[4])

    st.markdown("---")

    # Step selector
    step_options = {
        "1. Raw Data": "Original extracted data with issues",
        "2. Remove Duplicates": "Duplicate rows removed",
        "3. Format Columns": "Column names standardized",
        "4. Handle Nulls": "Missing values handled",
        "5. Format Types": "Data types converted",
        "6. Merge Data": "Datasets merged with state extraction"
    }

    selected_step = st.selectbox("Select transformation step:",
                                 list(step_options.keys()))

    st.markdown(f"### {selected_step}")
    st.markdown(step_options[selected_step])

    if selected_step == "1. Raw Data":
        col1, col2 = st.columns(2)
        with col1:
            render_dataframe_step(delay_steps[0], "Delay Data",
                                  "Raw data with duplicates and nulls")
        with col2:
            render_dataframe_step(airport_steps[0], "Airport Data",
                                  "Raw airport information")

    elif selected_step == "2. Remove Duplicates":
        col1, col2 = st.columns(2)
        with col1:
            render_dataframe_step(delay_steps[1], "Delay Data",
                                  "Duplicates removed using duplicated()")
        with col2:
            render_dataframe_step(airport_steps[1], "Airport Data",
                                  "Clean airport records")
        st.code("duplicated_rows = self.data.duplicated()\n"
                "self.clean_data = self.data[~duplicated_rows]",
                language='python')

    elif selected_step == "3. Format Columns":
        col1, col2 = st.columns(2)
        with col1:
            render_dataframe_step(delay_steps[2], "Delay Data",
                                  "Columns formatted to lowercase with "
                                  "underscores")
        with col2:
            render_dataframe_step(airport_steps[2], "Airport Data",
                                  "Consistent column naming")
        st.code("self.clean_data.columns = self.clean_data.columns."
                "str.lower().str.replace(' ', '_')", language='python')

    elif selected_step == "4. Handle Nulls":
        col1, col2 = st.columns(2)
        with col1:
            render_dataframe_step(delay_steps[3], "Delay Data",
                                  "Critical nulls dropped, others filled")
        with col2:
            render_dataframe_step(airport_steps[3], "Airport Data",
                                  "Missing values handled by type")
        st.code("self.clean_data = self.clean_data.dropna("
                "subset=self.crit_cols)\n"
                "self.clean_data[str_cols] = self.clean_data[str_cols]."
                "fillna('N/A')", language='python')

    elif selected_step == "5. Format Types":
        col1, col2 = st.columns(2)
        with col1:
            render_dataframe_step(delay_steps[4], "Delay Data",
                                  "Data types converted per configuration")
        with col2:
            render_dataframe_step(airport_steps[4], "Airport Data",
                                  "Final clean airport data")
        st.code("for col_key, dtype in type_mapping.items():\n"
                "    cols = self.col_types[col_key]\n"
                "    self.clean_data[cols] = self.clean_data[cols]."
                "astype(dtype)", language='python')

    elif selected_step == "6. Merge Data":
        render_dataframe_step(merged_data, "Merged Dataset",
                              "Final merged data with state extraction "
                              "and calculations")
        st.code("merged_df = delay_df.merge(airport_df, "
                "left_on='airport', right_on='iata', how='left')\n"
                "merged_df['state'] = merged_df['airport_name']."
                "str.split(', ').str[1]", language='python')

    # Function reference
    st.markdown("---")
    st.markdown("## Function Reference")

    transformer_methods = show_transformer_methods()
    merge_info = show_merge_function()

    with st.expander("View Transformer Class Methods"):
        for method_name, method_info in transformer_methods.items():
            st.markdown(f"**{method_name}**")
            st.markdown(method_info["description"])
            st.code(method_info["code"], language='python')
            st.markdown("---")

    with st.expander("View Merge Function"):
        st.markdown("**merge_main()**")
        st.markdown(merge_info["description"])
        st.code(merge_info["code"], language='python')
