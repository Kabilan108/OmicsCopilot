# src/schema/utils.py

import pandas as pd

from schema.datasets import Dataset


# TODO: Implement dataloaders in `omics` package
def load_data(dataset: Dataset) -> Dataset:
    """Load data for a dataset."""

    if dataset.type == "bulkrna":
        dataset.data = pd.read_csv(dataset.path)
    else:
        raise NotImplementedError

    return dataset
