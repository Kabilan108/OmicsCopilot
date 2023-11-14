# src/client/home.py

from rich.logging import RichHandler
from pydantic import BaseModel
import logging

import streamlit as st

# from client import settings
# from client.components import nav_page


# --------------------------------- Definitions ------------------------------ #


# --------------------------------- Setup ----------------------------------- #

# configure page
st.set_page_config(
    page_title="OmicsCopilot",
    page_icon="🧬",
    layout="wide",
)

# configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

# initialize session state
for key in ["dataset"]:
    if key not in st.session_state:
        st.session_state[key] = None


# -------------------------------- Sidebar ---------------------------------- #


# --------------------------------- Page ------------------------------------ #

st.write("# Welcome to OmicsCopilot! 👋")

st.markdown(
    """\
Streamlit is an open-source app built to help research scientists and
computational biologists analyze multi-omics data.

To get started, go to the **Sidebar** and select the **Data** tab to upload
your data or select from one of our curated datasets.
"""
)
