from enum import Enum
import pandas as pd
import streamlit as st

from nav_pages.graph import graph_display
from nav_pages.map import map_display


class ColorPalette(Enum):
    BACKGROUND = "#bccad6"
    PRIMARY = "#667292"
    SECONDARY = "#8d9db6"
    ACCENT = "#f1e3dd"


def navbar(data: pd.DataFrame):

    with st.container(key="navbar-container", border=None):
        page = st.radio(
            "Navigation",
            ["Home", "Graph", "Map"],
            horizontal=True,
            label_visibility="collapsed"
        )

    with st.container(key="bg"):
        if page == "Home":
            st.title("🏠 Home")
        elif page == "Graph":
            graph_display(data)
        elif page == "Map":
            map_display(data)
