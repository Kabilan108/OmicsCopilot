# src/client/app/pages/3_data_explorer.py

import pyarrow.parquet as pq
import pandas as pd
import requests

import streamlit as st

from io import BytesIO
import base64

from config import settings, logger, get_user
from components import nav_page


# --------------------------------- Definitions ------------------------------ #


# --------------------------------- Setup ----------------------------------- #

# configure page
st.set_page_config(
    page_title="explorer",
    page_icon="🧬",
    layout="wide",
)


# -------------------------------- Sidebar ---------------------------------- #


# --------------------------------- Page ------------------------------------ #

if get_user() is not None:
    st.write("# explorer")

    st.write(
        """
    Please upload your data or select from one of our curated datasets.
    """
    )


else:
    nav_page("")
    st.session_state.error = {
        "type": "auth",
        "detail": "You must be logged in to view this page.",
    }
