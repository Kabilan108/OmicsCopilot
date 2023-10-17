"""Entrypoint for OmicsCopilot"""


import streamlit as st

st.set_page_config(
    page_title="OmicsCopilot",
    page_icon="🧬",
)

st.write("# Welcome to OmicsCopilot! 👋")

st.markdown(
    """\
Streamlit is an open-source app framework built to help research scientists
and computational biologists analyze multi-omics data.
"""
)
