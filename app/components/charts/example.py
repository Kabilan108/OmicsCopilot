import json
import streamlit as st

from app.components.charts import volcano_plot


st.subheader("Visx-based Charts")


chart_data = volcano_plot(data={}, opts={}, key="volcano_plot")
st.markdown("Chart data:\n%s" % json.dumps(chart_data))
