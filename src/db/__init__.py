# src/db/__init__.py

# flake8: noqa E501

from pathlib import Path
import sqlite3

from data.schema import Dataset


MODULE_PATH = Path(__file__).parent
DB_PATH = MODULE_PATH / "datasets.db"


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
                path TEXT,
                id TEXT PRIMARY KEY
            )
        """
        )


def insert_dataset(dataset: Dataset):
    """Insert a dataset into the `datasets` table."""

    from sqlite3 import InterfaceError

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        try:
            cur.execute(
                """
                INSERT INTO datasets (name, type, metadata, path, id)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    dataset.name,
                    dataset.type.value,
                    dataset.metadata.model_dump_json(),
                    str(dataset.path),
                    dataset.id,
                ),
            )
        except InterfaceError as E:
            print("failed: ", E)
