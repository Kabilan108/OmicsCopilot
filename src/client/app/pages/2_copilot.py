# src/client/app/pages/2_copilot.py

import requests

import streamlit as st

from io import BytesIO
import base64

from config import settings, logger, get_user
from components import nav_page


# --------------------------------- Definitions ------------------------------ #


# --------------------------------- Setup ----------------------------------- #

st.set_page_config(
    page_title="copilot",
    page_icon="🧬",
    layout="wide",
)

# -------------------------------- Sidebar ---------------------------------- #


# --------------------------------- Page ------------------------------------ #

if get_user() is not None:
    st.write("# copilot")

    st.write("Chat with Copilot - Your pocket computational biologist")

else:
    nav_page("")
    st.session_state.error = {
        "type": "auth",
        "detail": "You must be logged in to view this page.",
    }
