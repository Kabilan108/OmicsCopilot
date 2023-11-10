# src/schema/datasets.py

# flake8: noqa E501

from abc import ABC, abstractmethod
from typing import List

from pydantic import BaseModel, Field


class Chunk(BaseModel, ABC):
    """A single text chunk from a paper."""

    @abstractmethod
    def __str__(self):
        """Return the text of the chunk."""
        pass


class MethodsSummary(BaseModel):
    """A detailed summary of the methods used to generate a dataset or perform some analysis."""

    # TODO: Add chain-of-destiny prompting to improve summarization

    summary: str = Field(
        ...,
        description="A detailed summary of the methods used to generate a dataset or perform some analysis.",
        examples=[
            """
        The BARRA:CuRDa dataset processing workflow starts with the curation of 17 handpicked RNA-seq datasets from the Gene Expression Omnibus (GEO). These datasets undergo quality control using FastQC, followed by trimming with Trimmomatic to remove low-quality bases and artifacts. The datasets are then subject to a secondary quality control phase to ensure the removal of ribosomal RNA and assess the transcript level abundance. Alignment and transcript quantification are done using STAR against the Homo sapiens reference genome from Ensembl (version GRCh38.94). The transcript-level abundance data are summarized into gene-level abundance estimates using the tximport package and DESeq2. This is followed by matrix transformation through the variance stabilizing transformation function of DESeq2 to prepare the final datasets suitable for downstream machine learning applications.
        """
        ],
    )
    tools: List[str] = Field(
        ...,
        description="A list of software tools or packages used by the authors.",
        examples=[
            [
                "GEO (Gene Expression Omnibus)",
                "FastQC",
                "Trimmomatic",
                "STAR",
                "Ensembl reference genome",
                "tximport",
                "DESeq2",
            ]
        ],
    )
    techniques: List[str] = Field(
        ...,
        description="A list of specific algorithms or techniques used by the authors.",
        examples=[
            [
                "Quality control",
                "Trimming of low-quality bases",
                "Removal of ribosomal RNA",
                "Alignment and transcript quantification",
                "Summarization of transcript-level abundance into gene-level abundance",
                "Matrix transformation via variance stabilizing transformation",
            ]
        ],
    )

    def __str__(self):
        return f"{self.summary}\n\ntools: {self.tools}\n\ntechniques: {self.techniques}\n\n"
