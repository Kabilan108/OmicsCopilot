# src/server/db/datasets.py

from sqlite3 import InterfaceError
from rich.console import Console
from pathlib import Path
from typing import List
import sqlite3
import json

from schema.datasets import Dataset
from db import DB_PATH


console = Console()


def create_table():
    """Create `datasets` table in `DB_PATH` database."""

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS datasets (
                name TEXT,
                type TEXT,
                metadata TEXT,
                methods TEXT,
                path TEXT,
                id TEXT PRIMARY KEY
            )
        """
        )


def insert_dataset(dataset: Dataset):
    """Insert a dataset into the `datasets` table."""

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        try:
            cur.execute(
                """
                INSERT INTO datasets (name, type, metadata, methods, path, id)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    dataset.name,
                    dataset.type.value,
                    dataset.metadata.model_dump_json(),
                    dataset.methods.model_dump_json(),
                    str(dataset.path),
                    dataset.id,
                ),
            )
        except InterfaceError as E:
            console.print(f"[red]Error:[/red] {E}")


def get_datasets() -> List[Dataset]:
    """Retrieve datasets from the `datasets` table."""

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM datasets")
        rows = cur.fetchall()

        datasets = []
        for row in rows:
            metadata = json.loads(row[2])
            methods = json.loads(row[3])
            dataset = Dataset(
                name=row[0],
                type=row[1],
                metadata=metadata,
                methods=methods,
                path=Path(row[4]),
                id=row[5],
            )
            datasets.append(dataset)

        return datasets


def get_dataset(id: str) -> Dataset:
    """Retrieve a dataset from the `datasets` table that matches the provided id."""

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        cur.execute("SELECT * FROM datasets WHERE id=?", (id,))

        row = cur.fetchone()

        if row is None:
            raise ValueError("No record found matching the provided id.")

        metadata = json.loads(row[2])
        methods = json.loads(row[3])
        dataset = Dataset(
            name=row[0],
            type=row[1],
            metadata=metadata,
            methods=methods,
            path=Path(row[4]),
            id=row[5],
        )

        return dataset
