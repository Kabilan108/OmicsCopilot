# schema/datasets.py

from typing import Any, Optional
from pathlib import Path
from enum import Enum

from pydantic import BaseModel, Field
import uuid

from schema.papers import MethodsSummary


class DatasetType(str, Enum):
    """The specific sequencing technology used to generate the data."""

    bulkrna = "bulkrna"
    scrna = "scrna"
    ma = "ma"


class Metadata(BaseModel):
    """Metadata for a dataset."""

    gse: Optional[str] = Field(
        None,
        description="The GEO Series accession number for the dataset.",
        examples=["GSE123456"],
    )
    tissue: Optional[str] = Field(
        None,
        description="The tissue from which the sample was taken.",
        examples=["brain", "liver", "heart"],
    )
    genes: Optional[int] = Field(
        None,
        description="The number of genes in the dataset.",
        examples=[20000],
    )
    samples: Optional[int] = Field(
        None,
        description="The number of samples/subjects/patients in the dataset.",
        examples=[100],
    )
    classes: Optional[int] = Field(
        None,
        description="The number of classes (or groups) in the dataset.",
        examples=[2],
    )


class Dataset(BaseModel):
    """A dataset with genomic data."""

    name: str = Field(
        ...,
        description="A descriptive identifier for the dataset.",
        examples=["GSE123456 - Bulk RNA-seq of human brain tissue"],
    )
    type: DatasetType = Field(
        ...,
        description="The specific sequencing technology used to generate the data.",
        examples=["bulkrna", "scrna", "ma"],
    )
    metadata: Metadata = Field(
        ...,
        description="Metadata about the dataset.",
        examples=[{}],
    )
    methods: Optional[MethodsSummary] = Field(
        None,
        description="A detailed summary of the methods used to generate a dataset or perform some analysis.",
        examples=[{}],
    )
    path: Optional[str | Path] = Field(
        None,
        description="The path to the dataset's data file. This should be a CSV file.",
        examples=["/path/to/dataset.csv"],
    )
    link: Optional[str] = Field(
        None,
        description="A link to the dataset's data file.",
        examples=["https://www.example.com/path/to/dataset.csv"],
    )
    data: Optional[Any] = Field(
        None,
        description="The dataset's genomic data as a Pandas DataFrame.",
    )
    id: Optional[str] = Field(
        None,
        description="A unique identifier for the dataset.",
    )

    def __init__(self, **data):
        super().__init__(**data)
        self.id = self.id or self.generate_id()

    def generate_id(self):
        """Generate a unique identifier for the dataset."""
        return str(
            uuid.uuid5(
                uuid.NAMESPACE_OID,
                f"{self.name}-{self.type}-{self.metadata.model_dump()}",
            )
        )

    class Config:
        arbitrary_types_allowed = True
