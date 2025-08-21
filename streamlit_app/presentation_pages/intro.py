import streamlit as st


def pres_intro():
    # HTML file is largely AI generated
    with open("presentation_pages/intro.html") as f:
        st.markdown(f.read(), unsafe_allow_html=True)