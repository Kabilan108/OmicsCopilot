# src/server/routes/datasets.py

from fastapi import APIRouter, Depends, HTTPException
from starlette.concurrency import run_in_threadpool
import pyarrow.parquet as pq
import pyarrow as pa
import pandas as pd

from typing import List
from io import BytesIO
import base64

from schema.datasets import Dataset
from schema import utils
import db.datasets as db


async def load_data_threadpool(id: str):
    """Load data asynchronously"""
    dataset = db.get_dataset(id)
    if dataset:
        dataset = await run_in_threadpool(utils.load_data, dataset)

    return dataset


def df_to_parquet(df: pd.DataFrame) -> str:
    """Convert a pandas DataFrame to parquet."""
    io = BytesIO()
    table = pa.Table.from_pandas(df)
    pq.write_table(table, io)
    pq_data = io.getvalue()
    data = base64.b64encode(pq_data).decode()

    return data


router = APIRouter(
    prefix="/datasets",
    tags=["datasets"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Dataset])
async def list_datasets() -> List[Dataset]:
    """Get list of all curated datasets."""

    return db.get_datasets()


@router.get("/{id}", response_model=Dataset)
async def get_dataset(
    id: str, dataset: Dataset = Depends(load_data_threadpool)
) -> Dataset:
    """Get a curated dataset."""

    if dataset is None:
        raise HTTPException(status_code=404, detail="Dataset not found")

    dataset.data = df_to_parquet(dataset.data)

    return dataset


# TODO: Add /upload endpoint
#       This will be used to upload a dataset to the server
#       and return a unique identifier for the dataset.
#       The dataframe should be cached in the server somewhere so that analysis
#       can be performed on it.
