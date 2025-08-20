import streamlit as st

from navbar import navbar
from util import get_data, AccessType


def main():
    # Center all content
    with open("styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    with st.container(key="title"):
        st.title("Airport Delay Stats")
    data = get_data(AccessType.FILE)
    navbar(data)



if __name__ == "__main__":
    st.set_page_config(
        page_title="BluckBoster Analytics",
        layout="wide"
    )
    main()
