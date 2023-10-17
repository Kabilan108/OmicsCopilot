import React from "react"
import ScatterPlot from "./components/plots/ScatterPlot"

export default function App() {
  return (
    <div
      style={{
        height: "600px",
        width: "100%",
        position: "relative",
      }}
    >
      <ScatterPlot />
    </div>
  )
}
