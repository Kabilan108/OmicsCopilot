# src/client/components/charts/deg.py

import re
import os
import pickle
import GEOparse
import numpy as np
import pandas as pd
import tempfile as temp

from statsmodels.stats import multitest
from scipy import stats


_parent_dir = os.path.dirname(os.path.abspath(__file__))
datapath = os.path.join(_parent_dir, "frontend/public/deg.csv")

p_thr = 0.05
fc_thr = 2


def tempdir(dirname: str):
    """
    Create path to a temporary directory
    @param dirname
        name of temporary directory
    @return
        path to temporary directory
    """

    name = os.path.join(temp.gettempdir().replace("\\", "/"), dirname)
    if not os.path.isdir(name):
        os.mkdir(name)
    return name


def geodlparse(acc: str):
    """
    Download, parse and cache data from GEO
    @param acc
        A GEO accession
    @return
        a GSE or GPL object
    """

    # Path to temporary directory
    geodir = tempdir("GEO")

    # Download files
    try:
        # Specify file names
        names = [f"{acc}.txt", f"{acc}_family.soft.gz"]
        geofile = os.path.join(geodir, names[0 if acc[:3] == "GPL" else 1])
        cachefile = os.path.join(geodir, f"{acc}.pkl")

        if os.path.isfile(cachefile):
            # Load data if it has already been cached
            try:
                print("Loading cached data...")
                with open(cachefile, "rb") as cache:
                    geodata = pickle.load(cache)
                return geodata
            except Exception as e:
                print(f"ERROR: Loading cached file failed.\n{e}")
        else:
            if os.path.isfile(geofile):
                # If data has already been downloaded, parse it and cache results
                print("Already downloaded. Parsing...")
                geodata = GEOparse.get_GEO(filepath=geofile, silent=True)
            else:
                # Download and parse data
                print("Downloading and parsing...")
                geodata = GEOparse.get_GEO(acc, destdir=geodir, silent=True)
            # Cache data
            with open(cachefile, "wb") as cache:
                pickle.dump(geodata, file=cache)
            return geodata
    except Exception as e:
        print(f"ERROR: Enter a valid GEO Accension\n{e}")


def main():
    # Download and parse GSE and GPL data
    gse = geodlparse("GSE17257")
    gpl = geodlparse(*gse.metadata["platform_id"])

    # Prepare dataframe with expression values
    gse_data = pd.concat(
        [gsm.table.set_index("ID_REF")["VALUE"] for _, gsm in gse.gsms.items()], axis=1
    ).set_axis([x for x, _ in gse.gsms.items()], axis=1)

    # Merge gse data with genes from the GPL
    gse_data = (
        gse_data.merge(
            gpl.table[["ID", "Gene Symbol"]], how="left", left_index=True, right_on="ID"
        )
        .rename({"ID_REF": "ID", "Gene Symbol": "Gene"}, axis=1)
        .set_index(["ID", "Gene"])
        .sort_index(axis=1)
    )

    # Label columns as 'Control' or 'Clioquinol'
    columns = (
        gse.phenotype_data["title"]
        .apply(lambda x: re.search(r"DMSO|CQ", x)[0])
        .replace({"DMSO": "Control", "CQ": "Clioquinol"})
        .sort_index()
        .reset_index()
    )
    gse_data.columns = [columns["index"].values, columns["title"].values]

    # Compute the (signed) fold change (Clioquinol / Control)
    deg = gse_data.groupby(lambda x: x[1], axis=1).mean()
    FC = (deg["Clioquinol"] / deg["Control"]).values
    pval = stats.ttest_ind(
        gse_data.loc[:, gse_data.columns.get_level_values(1) == "Clioquinol"].values,
        gse_data.loc[:, gse_data.columns.get_level_values(1) == "Control"].values,
        axis=1,
    ).pvalue
    adj_pval = multitest.fdrcorrection(pval)[1]

    deg["log2FC"] = np.log2(FC)
    deg["pval"] = pval
    deg["adj_pval"] = adj_pval
    deg["neglog10_pval"] = -np.log10(deg["adj_pval"])

    # Remove any probes with no Gene symbols mapped
    deg = (
        deg.iloc[:, 2:]
        .reset_index()
        .dropna(subset="Gene")
        .reset_index(drop=True)
        .rename({"ID": "probe", "Gene": "gene"}, axis=1)
    )

    logfc_thr = np.log2(fc_thr)
    I_sig = deg["adj_pval"] <= p_thr
    I_up = deg["log2FC"] >= logfc_thr
    I_down = deg["log2FC"] <= -logfc_thr

    deg["sig"] = "not significant"
    deg.loc[I_sig & I_up, "sig"] = "upregulated"
    deg.loc[I_sig & I_down, "sig"] = "downregulated"

    # Save results
    deg.to_csv(datapath, index=False)


if __name__ == "__main__":
    main()
