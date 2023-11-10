# src/client/home.py

import streamlit as st

# from app import settings
# from app.components import nav_page


# -- Definitions -- #


# ---- Sidebar ---- #


# -- Page Setup --- #
st.set_page_config(
    page_title="OmicsCopilot",
    page_icon="🧬",
)

st.write("# Welcome to OmicsCopilot! 👋")

st.markdown(
    """\
Streamlit is an open-source app built to help research scientists and
computational biologists analyze multi-omics data.

To get started, go to the **Sidebar** and select the **Data** tab to upload
your data or select from one of our curated datasets.
"""
)
