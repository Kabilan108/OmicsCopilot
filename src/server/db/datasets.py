# src/server/db/datasets.py

from supabase import PostgrestAPIError

from typing import List

from api import logger
from db import supabase
from schema.datasets import Dataset


def _exists() -> bool:
    """Check if the `datasets` table exists in the database."""
    return True


def insert_dataset(dataset: Dataset | List[Dataset]):
    """Insert a dataset into the `datasets` table."""

    if _exists() is False:
        logger.error("[red]Insert failed.[/red] The `datasets` table does not exist.")
        return False

    try:
        if isinstance(dataset, Dataset):
            dataset = dataset.db_dump()
        else:
            dataset = [ds.db_dump() for ds in dataset]

        supabase.table("datasets").insert(dataset).execute()

        return True

    except PostgrestAPIError as e:
        logger.error(f"[red]Insert failed.[/red] {e}")
        return False


def get_datasets() -> List[Dataset]:
    """Retrieve datasets from the `datasets` table."""

    try:
        data, _ = supabase.table("datasets").select("*").execute()
        return [Dataset(**ds) for ds in data]
    except PostgrestAPIError as e:
        logger.error(f"[red]Select failed.[/red] {e}")
        return []


def get_dataset(id_: str) -> Dataset:
    """Retrieve a dataset from the `datasets` table that matches the provided id."""

    try:
        data, _ = supabase.table("datasets").select("*").eq("id", id_).execute()
        assert len(data[-1]) == 1
        return Dataset(**data[-1][0])
    except PostgrestAPIError as e:
        logger.error(f"[red]Select failed.[/red] {e}")
        return None
    except AssertionError:
        logger.error(f"[red]Select failed.[/red] No dataset with id {id_} exists.")
        return None
