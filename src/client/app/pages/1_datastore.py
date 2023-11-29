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

    # return [Dataset(**ds) for ds in response.json()]
    return {ds["id"]: Dataset(**ds) for ds in response.json()}


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

datasets = list_datasets()


# -------------------------------- Sidebar ---------------------------------- #

with st.sidebar.form(key="dataset-form"):
    upload_dataset = st.file_uploader(
        label="Upload a dataset",
        accept_multiple_files=False,
        type=["csv", "tsv", "txt"],
        help="Upload a dataset to analyze. The first row should contain column names.",
        disabled=True,
    )

    selected_dataset = st.selectbox(
        label="Select a dataset",
        options=list(datasets.keys()),
        format_func=lambda x: datasets[x].name,
    )

    load_btn = st.form_submit_button(
        label="Load dataset",
    )

with st.sidebar.form(key="qc-form"):
    run_pca = st.checkbox(
        label="Run PCA",
        value=True,
    )

    run_tsne = st.checkbox(
        label="Run t-SNE",
        value=True,
    )

    run_umap = st.checkbox(
        label="Run UMAP",
        value=True,
    )

    run_btn = st.form_submit_button(
        label="Run QC",
    )

if upload_dataset:
    st.write(f"you uploaded: {upload_dataset.name}")
    # TODO: Save dataset to server

if load_btn:
    logger.info(f"retrieving {selected_dataset}")
    dataset = get_dataset(selected_dataset)

    st.session_state.dataset = dataset


# --------------------------------- Page ------------------------------------ #

if get_user() is not None:
    st.write("# datastore")

else:
    nav_page("")
    st.session_state.error = {
        "type": "auth",
        "detail": "You must be logged in to view this page.",
    }
