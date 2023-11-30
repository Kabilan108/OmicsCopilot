# src/client/app/pages/1_datastore.py

import pyarrow.parquet as pq
import pandas as pd
import requests

import streamlit as st

from io import BytesIO
import base64

from config import settings, logger, get_user
from schema.datasets import Dataset
from components import nav_page


# --------------------------------- Definitions ------------------------------ #


def list_datasets():
    """Get list of all curated datasets."""
    response = requests.get(f"{settings.API_BASE}/datasets")
    response.raise_for_status()

    return pd.DataFrame(response.json())


def get_dataset(id: str) -> Dataset:
    """Get a curated dataset and convert it to a pandas DataFrame."""

    response = requests.get(f"{settings.API_BASE}/datasets/{id}")
    response.raise_for_status()

    dataset = Dataset(**response.json())
    parquet_data = base64.b64decode(dataset.data)
    dataset.data = pq.read_table(BytesIO(parquet_data)).to_pandas()

    return dataset


# --------------------------------- Setup ----------------------------------- #

st.set_page_config(
    page_title="datastore",
    page_icon="🧬",
    layout="wide",
)

if get_user() is not None:
    datasets = list_datasets()

# -------------------------------- Sidebar ---------------------------------- #


# --------------------------------- Page ------------------------------------ #

if get_user() is not None:
    st.write("# datastore")

    tabs = st.tabs(["Datasets", "Literature"])

    with tabs[0]:
        st.write("## Datasets")

        st.write("The following datasets are available for analysis.")

        st.dataframe(
            data=datasets,
            use_container_width=True,
            hide_index=True,
            column_order=["name", "type", "link"],
        )

        with st.form(key="dataset-form"):
            selected_dataset = st.selectbox(
                label="Select a dataset",
                index=None,
                options=datasets["id"].tolist(),
                format_func=lambda x: datasets[datasets["id"] == x]["name"].values[0],
            )

            upload_dataset = st.file_uploader(
                label="Upload a dataset",
                accept_multiple_files=False,
                type=["csv", "tsv", "txt"],
                help="Upload a dataset to analyze. The first row should contain column names.",
                disabled=True,
            )

            load = st.form_submit_button(
                label="Load dataset",
            )

    with tabs[1]:
        st.write("## Literature")
        st.write("The following literature is available for analysis.")

    if load:
        logger.info(f"retrieving {selected_dataset}")
        dataset = get_dataset(selected_dataset)

        logger.info(f"loaded {selected_dataset}")
        st.success(f"loaded {selected_dataset}")
        st.session_state.dataset = dataset

else:
    nav_page("")
    st.session_state.error = {
        "type": "auth",
        "detail": "You must be logged in to view this page.",
    }
