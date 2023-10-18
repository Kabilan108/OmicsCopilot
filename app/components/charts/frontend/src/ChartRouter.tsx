import React from "react"
import VolcanoPlot from "./VolcanoPlot"
// import Heatmap from './Heatmap'; // Import your Heatmap component
import ParentSize from "@visx/responsive/lib/components/ParentSize"
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"

interface Args {
  chart_type: "volcano_plot" | "heatmap" | "my_component"
  data: []
  opts: object
}

class ChartRouter extends StreamlitComponentBase<Args> {
  componentDidMount() {
    Streamlit.setFrameHeight()
  }

  componentDidUpdate() {
    Streamlit.setFrameHeight()
  }

  render() {
    const { chart_type, data, opts } = this.props.args

    switch (chart_type) {
      case "volcano_plot":
        return (
          <>
            <ParentSize>
              {({ width, height }) => (
                <VolcanoPlot
                  data={data}
                  opts={opts}
                  width={width}
                  height={height}
                />
              )}
            </ParentSize>
          </>
        )
      //   case 'heatmap':
      //     return <Heatmap data={data} opts={opts as HeatmapOpts} />;
      default:
        return <div>Invalid chart type</div>
    }
  }
}

export default withStreamlitConnection(ChartRouter)
