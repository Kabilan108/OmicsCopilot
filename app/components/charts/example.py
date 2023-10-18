import json
import pandas as pd
import streamlit as st

from app.components.charts import volcano_plot

st.subheader("Visx-based Charts")

chart_type = st.selectbox("Select chart type", ("volcano_plot", "heatmap", "fail"))

data = pd.read_csv("components/charts/frontend/public/deg.csv")

if chart_type == "volcano_plot":
    chart_data = volcano_plot(data, opts={}, key="volcano_plot")
else:
    chart_data = {"error": "No chart selected"}

st.markdown("Chart data:  %s" % json.dumps(chart_data))
