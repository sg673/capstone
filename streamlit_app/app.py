import streamlit as st

from navbar import navbar
from util import get_data, AccessType


def main():
    # Center all content
    st.set_page_config(page_title="Airport Delays", layout="wide")
    with open("styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    data = get_data(AccessType.FILE)
    with st.container(key="title"):
        st.title("Airport Delay Stats")
    navbar(data)


if __name__ == "__main__":
    st.set_page_config(
        page_title="BluckBoster Analytics",
        layout="wide"
    )
    main()
