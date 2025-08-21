import streamlit as st


def pres_conc():
    # HTML file is largely AI generated
    with open("presentation_pages/conclusion.html") as f:
        st.markdown(f.read(), unsafe_allow_html=True)
