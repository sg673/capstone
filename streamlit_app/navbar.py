from enum import Enum
import pandas as pd
import streamlit as st

from nav_pages.graph import graph_display
from nav_pages.map import map_display

from presentation_pages.intro import pres_intro
from presentation_pages.extract import pres_extract
from presentation_pages.transform import pres_transform
from presentation_pages.load import pres_load
from presentation_pages.visual import pres_visual
from presentation_pages.conc import pres_conc


class ColorPalette(Enum):
    BACKGROUND = "#bccad6"
    PRIMARY = "#667292"
    SECONDARY = "#8d9db6"
    ACCENT = "#f1e3dd"


def navbar(data: pd.DataFrame, raw_data):

    with st.container(key="navbar-container", border=None):
        page = st.radio(
            "Navigation",
            ["Home",
             "Intro",
             "Extract",
             "Transform",
             "Load",
             "Visualise",
             "Conclusion"],
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
        elif page == "Intro":
            pres_intro()
        elif page == "Extract":
            pres_extract(raw_data[1], raw_data[0])
        elif page == "Transform":
            pres_transform()
        elif page == "Load":
            pres_load()
        elif page == "Visualise":
            pres_visual()
        elif page == "Conclusion":
            pres_conc()
