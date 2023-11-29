# src/server/rag/parsing.py

from typing import Any, List, Optional

from pydantic import BaseModel
import pandas as pd


class TableColumnOutput(BaseModel):
    """Output from analyzing a table column."""

    col_name: str
    col_type: str
    summary: Optional[str] = None

    def __str__(self) -> str:
        return (
            f"Column: {self.col_name}\nType: {self.col_type}\nSummary: {self.summary}\n"
        )


class TableOutput(BaseModel):
    """Output from analyzing a table."""

    summary: str
    columns: List[TableColumnOutput]


class Element(BaseModel):
    """Element object wrapper for Unstructured.io"""

    id: str
    type: str
    element: Any
    image_path: Optional[str] = None
    table_output: Optional[TableOutput] = None
    table: Optional[pd.DataFrame] = None

    class Config:
        arbitrary_types_allowed = True


def html_to_df(html_str: str) -> pd.DataFrame:
    """Convert HTML to dataframe."""
    from lxml import html

    tree = html.fromstring(html_str)
    table_element = tree.xpath("//table")[0]
    rows = table_element.xpath(".//tr")

    data = []
    for row in rows:
        cols = row.xpath(".//td")
        cols = [c.text.strip() if c.text is not None else "" for c in cols]
        data.append(cols)

    return pd.DataFrame(data[1:], columns=data[0])
