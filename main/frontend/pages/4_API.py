import streamlit as st

st.title("German Accidents API")

st.info("Click below to open API documentation")

st.link_button(
    "OpenAPI UI",
    "http://127.0.0.1:8000/docs"
)