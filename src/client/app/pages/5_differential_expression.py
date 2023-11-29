# src/client/app/pages/5_differential_expression.py

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
    page_title="differential expression",
    page_icon="🧬",
    layout="wide",
)


# -------------------------------- Sidebar ---------------------------------- #


# --------------------------------- Page ------------------------------------ #

if get_user() is not None:
    st.write("# differential expression")

else:
    nav_page("")
    st.session_state.error = {
        "type": "auth",
        "detail": "You must be logged in to view this page.",
    }
