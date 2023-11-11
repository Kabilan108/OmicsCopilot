# src/client/components/charts/__init__.py

import os

import pandas as pd
import streamlit.components.v1 as components


_DEBUG = False

if _DEBUG:
    _visx = components.declare_component(
        "visx",
        url="http://localhost:3001",
    )
else:
    _parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(_parent_dir, "frontend/build")
    _visx = components.declare_component("visx", path=build_dir)


def volcano_plot(
    data: pd.DataFrame,
    key: str = None,
    xaxis: str = "log2FC",
    yaxis: str = "neglog10_pval",
    xaxis_label: str = "log2 (fold change)",
    yaxis_label: str = "-log10 (p-value)",
    pval_cutoff: float = 0.05,
    fc_cutoff: float = 2,
) -> dict:
    """Create a volcano plot.

    Parameters
    ----------
    data : pd.DataFrame
        Dataframe with columns "probe", "gene", "log2FC", "pval", "adj_pval",
        and "sig"
    opts : dict
        Dictionary of options for the chart
    key : str, optional
        Unique key for the chart, by default None

    Returns
    -------
    dict
        Dictionary of chart data
    """

    data = data.dropna()

    data = data.to_dict(orient="records")

    opts = {
        "xaxis": xaxis,
        "yaxis": yaxis,
        "xaxis_label": xaxis_label,
        "yaxis_label": yaxis_label,
        "pval_cutoff": pval_cutoff,
        "fc_cutoff": fc_cutoff,
    }

    return _visx(chart_type="volcano_plot", data=data, opts=opts, key=key)
