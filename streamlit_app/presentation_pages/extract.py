import streamlit as st
import pandas as pd
import os


# ✅ CSS (only once, at the start of your app)
st.markdown("""
<style>
  .df-container {
    margin: 1.5rem 0;
    background: white;
    padding: 1rem;
    border-radius: 12px;
    box-shadow: 0px 3px 3px var(--primary);
    overflow-x: hidden;
    width: 100%;
  }

  table {
    border-collapse: collapse;
    width: 100%;
    table-layout: fixed;
  }

  table th, table td {
    padding: 8px 12px;
    border: 1px solid #ddd;
    text-align: left;
    word-wrap: break-word;
    max-width: 200px;
  }

  table th {
    background-color: var(--secondary);
    color: white;
  }

  .expander {
    margin: 1rem 0;
    background: var(--accent);
    padding: 1rem;
    border-radius: 10px;
    cursor: pointer;
  }

  .expander-content {
    display: none;
    margin-top: 1rem;
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 1px 4px rgba(0,0,0,0.1);
  }

  .expander.active .expander-content {
    display: block;
  }

  pre {
    background: #2d2d2d;
    color: #f8f8f2;
    padding: 1rem;
    border-radius: 10px;
    overflow-x: auto;
  }

  code {
    font-family: "Courier New", monospace;
  }

  .two-col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 2rem;
  }
</style>
""", unsafe_allow_html=True)


def render_dataframe(df: pd.DataFrame, max_rows=5):
    """Convert a Pandas DataFrame into a styled HTML table."""
    if df is None or df.empty:
        return "<p><i>No data available</i></p>"

    st.dataframe(
        df.head(max_rows),
        use_container_width=True,
        height=min(400, (max_rows + 1) * 35)
    )


def pres_extract(delay_df=None, airport_df=None):
    st.markdown("""
    <header>
      <h1>Extract Phase</h1>
      <h2>Data Collection and Initial Processing</h2>
    </header>
    """, unsafe_allow_html=True)
    with st.expander("Raw Data"):
        st.markdown("<h2>Raw Data Samples</h2>", unsafe_allow_html=True)

        # Airline Delay Data
        st.markdown("<h3>Airline Delay Cause Data</h3>", unsafe_allow_html=True)
        if delay_df is not None:
            st.markdown(f"<b>Shape:</b> {delay_df.shape[0]} rows × {delay_df.shape[1]} columns", unsafe_allow_html=True)
            render_dataframe(delay_df)
        else:
            st.warning("Airline delay data not available.")

        st.markdown("---")

        # Airport Data
        st.markdown("<h3>Airport Information Data</h3>", unsafe_allow_html=True)
        if airport_df is not None:
            st.markdown(f"<b>Shape:</b> {airport_df.shape[0]} rows × {airport_df.shape[1]} columns", unsafe_allow_html=True)
            render_dataframe(airport_df)
        else:
            st.warning("Airport data not available.")
