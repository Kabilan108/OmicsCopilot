# data/download.py

# flake8: noqa E501

from rich.progress import Progress
from rich.console import Console
import requests
import click

from pathlib import Path
from typing import List
import zipfile

from data import MODULE_PATH
from data.schema import Dataset, DatasetType
import db.datasets as db


console = Console()


def _get_BARRA_CuRDa(format: str = "csv") -> List[Dataset]:
    """Retrieve links to BARRA:CuRDa data files [1].

    Args:
        format: Data file format. Defaults to "csv".
                Allows: csv, tab, arff, pca, tsne, results
    Returns:
        dict: Dictionary of links to BARRA:CuRDa data files
    References:
        [1] Feltes, B.C.; Poloni, J.F.; Dorn, M. Benchmarking and Testing Machine Learning Approaches with BARRA:CuRDa, a Curated RNA-Seq Database for Cancer Research. Journal of Computational Biology. 2021 Sep; 28(9), 931-944.
    """

    # Construct the dataset URL directly
    base_url = "https://sbcb.inf.ufrgs.br"
    dataset_url = "https://gist.githubusercontent.com/mateuz/f87fb07050926705368c6934ddc77524/raw/47063780a3cdaf671d3e678d90fcc41e73754c3c/barracurda.json"

    # Make a GET request to fetch the dataset JSON
    response = requests.get(dataset_url)
    response.raise_for_status()

    # Parse the JSON response
    datasets = response.json()

    return [
        Dataset(
            name=f"BARRA:CuRDa - {ds['gse']} - {ds['tissue']}",
            type=DatasetType.bulkrna,
            metadata={
                "gse": ds["gse"],
                "tissue": ds["tissue"],
                "genes": ds["genes"],
                "samples": ds["samples"],
                "classes": ds["classes"],
            },
            link=f"{base_url}{ds['downloads'][format]}",
        )
        for ds in datasets
    ]


def download_BARRA_CuRDa(path: Path | str = None, verbose: bool = True) -> bool:
    """Download BARRA:CuRDa data files [1].

    Args:
        path (Path | str, optional): Path to store data files. Defaults to "MODULE_PATH/BARRA_CuRDa".
        verbose (bool, optional): Print verbose output. Defaults to True.
    Returns:
        bool: True if successful, False otherwise.
    """

    if path is None or path == "":
        path = MODULE_PATH / "BARRA_CuRDa"
    else:
        path = Path(path)

    if not path.exists():
        path.mkdir()

    datasets = _get_BARRA_CuRDa()

    db.create_table()

    progress = Progress()
    progress_bar = None

    try:
        with progress:
            for ds in progress.track(datasets, description="Downloading datasets..."):
                ds.path = path / f"{ds.link.split('/')[-1]}"

                if verbose:
                    progress_bar = progress.add_task(
                        f"Downloading {ds.name}...", total=100
                    )

                with requests.get(ds.link, stream=True) as r:
                    r.raise_for_status()
                    with open(ds.path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)
                                if verbose:
                                    progress.advance(progress_bar, len(chunk))

                # Extract the CSV file from the downloaded ZIP file
                with zipfile.ZipFile(ds.path, "r") as zip_ref:
                    csv_file = [f for f in zip_ref.namelist() if f.endswith(".csv")][0]
                    zip_ref.extract(csv_file, path)

                # Remove the downloaded ZIP file
                ds.path.unlink()

                # Insert the dataset into the database
                db.insert_dataset(ds)

                if verbose:
                    progress.print(f"Downloaded '{ds.name}'.")
                    progress.remove_task(progress_bar)

    except KeyboardInterrupt:
        console.print("Download process interrupted.")
        return False

    return True


@click.command()
@click.argument("dataset")
@click.option("--path", "-p", default=None, help="Path to store data files.")
@click.option("--verbose", "-v", is_flag=True, help="Print verbose output.")
def main(dataset, path, verbose):
    """Download datasets."""
    if dataset == "barra-curda":
        download_BARRA_CuRDa(path=path, verbose=verbose)
    else:
        console.print(f"Dataset {dataset} is not available.")


if __name__ == "__main__":
    main()
