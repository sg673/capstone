import streamlit as st
import pandas as pd
import os
from datetime import datetime


def show_csv_loader():
    """Display CSV loading functionality"""
    return {
        "description": "Save processed data to CSV files with timestamp",
        "code": '''def save_to_csv(self, data: pd.DataFrame, filename: str):
    """Save DataFrame to CSV with timestamp"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = f"data/output/{filename}_{timestamp}.csv"
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    data.to_csv(output_path, index=False)
    
    self.logger.info(f"Data saved to {output_path}")
    return output_path'''
    }


def show_db_loader():
    """Display database loading functionality"""
    return {
        "description": "Load data to PostgreSQL database with error handling",
        "code": '''def load_to_database(self, data: pd.DataFrame, table_name: str):
    """Load DataFrame to PostgreSQL database"""
    try:
        # Create connection
        engine = create_engine(self.db_config['connection_string'])
        
        # Load data with replace strategy
        data.to_sql(table_name, engine, 
                   if_exists='replace', 
                   index=False, 
                   method='multi')
        
        self.logger.info(f"Loaded {len(data)} rows to {table_name}")
        return True
        
    except Exception as e:
        self.logger.error(f"Database load failed: {e}")
        return False'''
    }





def simulate_load_process():
    """Simulate the loading process"""
    # Sample processed data
    sample_data = pd.DataFrame({
        'year': [2023, 2023, 2023],
        'month': [1, 1, 2],
        'carrier': ['AA', 'DL', 'UA'],
        'carrier_name': ['American Airlines', 'Delta Air Lines', 'United Airlines'],
        'iata': ['JFK', 'LAX', 'ORD'],
        'state': ['NY', 'CA', 'IL'],
        'arr_flights': [1000, 1200, 950],
        'total_ct': [150, 180, 120],
        'arr_flights_pct': [15.0, 15.0, 12.6]
    })
    
    return sample_data


def render_load_metrics(data, load_type):
    """Display load operation metrics"""
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Records", f"{len(data):,}")
    with col2:
        st.metric("Columns", data.shape[1])
    with col3:
        st.metric("Size (KB)", f"{data.memory_usage(deep=True).sum() // 1024}")
    with col4:
        if load_type == "CSV":
            st.metric("Files", "1")
        else:
            st.metric("Tables", "1")


def pres_load():
    st.markdown("""
    <header>
      <h1>Load Phase</h1>
      <h2>Data Storage and Persistence</h2>
    </header>
    """, unsafe_allow_html=True)

    # Load sample processed data
    sample_data = simulate_load_process()
    
    st.markdown("---")
    
    # Load type selector
    load_options = {
        "CSV Loading": "Save processed data to CSV files",
        "Database Loading": "Load data to PostgreSQL database"
    }
    
    selected_option = st.selectbox("Select load operation:", 
                                   list(load_options.keys()))
    
    st.markdown(f"### {selected_option}")
    st.markdown(load_options[selected_option])
    
    if selected_option == "CSV Loading":
        st.markdown("#### CSV File Output")
        
        # Show CSV loader code
        csv_info = show_csv_loader()
        st.code(csv_info["code"], language='python')
        
        # Simulate CSV save
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Sample Output Data**")
            st.dataframe(sample_data, use_container_width=True, height=200)
        
        with col2:
            st.markdown("**Load Metrics**")
            render_load_metrics(sample_data, "CSV")
        
        # File structure
        st.markdown("**Output File Structure**")
        st.code("""
data/output/
├── merged_data_20241201_143022.csv
├── delay_summary_20241201_143022.csv
└── airport_stats_20241201_143022.csv
        """)
        
        # Benefits
        st.markdown("**CSV Loading Benefits:**")
        st.markdown("""
        - ✅ Simple file-based storage
        - ✅ Easy to share and backup
        - ✅ No database dependencies
        - ✅ Timestamped versions
        """)
    
    elif selected_option == "Database Loading":
        st.markdown("#### PostgreSQL Database")
        
        # Show database loader code
        db_info = show_db_loader()
        st.code(db_info["code"], language='python')
        
        # Simulate database load
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Data to Load**")
            st.dataframe(sample_data, use_container_width=True, height=200)
        
        with col2:
            st.markdown("**Load Metrics**")
            render_load_metrics(sample_data, "Database")
        
        # Database schema
        st.markdown("**Database Schema**")
        st.code("""
CREATE TABLE airport_delays (
    year INTEGER,
    month INTEGER,
    carrier VARCHAR(10),
    carrier_name VARCHAR(100),
    iata VARCHAR(10),
    state VARCHAR(10),
    arr_flights INTEGER,
    total_ct INTEGER,
    arr_flights_pct DECIMAL(5,2)
);
        """, language='sql')
        
        # Benefits
        st.markdown("**Database Loading Benefits:**")
        st.markdown("""
        - ✅ Structured data storage
        - ✅ Query capabilities
        - ✅ Data integrity constraints
        - ✅ Concurrent access support
        """)
    

    
    # Load Strategy and Summary from HTML
    st.markdown("---")
    
    # Read and display HTML content
    try:
        with open("presentation_pages/load_summary.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        st.markdown(html_content, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Load summary HTML file not found")