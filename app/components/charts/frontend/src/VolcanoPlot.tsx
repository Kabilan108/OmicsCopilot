import React, { useMemo, useCallback, useRef } from "react"
import { extent, format } from "d3"
import { Zoom } from "@visx/zoom"
import { Group } from "@visx/group"
import { localPoint } from "@visx/event"
import { Line, Circle } from "@visx/shape"
import { Axis, AxisLeft } from "@visx/axis"
// import { CircleClipPath } from "@visx/clip-path"
import { GridColumns, GridRows } from "@visx/grid"
import { withTooltip, Tooltip } from "@visx/tooltip"
import { scaleLinear, scaleOrdinal } from "@visx/scale"
import { LegendOrdinal, LegendItem, LegendLabel } from "@visx/legend"

interface Data {
  probe: string
  gene: string
  log2FC: number
  pval: number
  adj_pval: number
  sig: string
  neglog10_pval: number
  type: string
  tooltip_value: string
}

interface ToolTipData {
  probe?: string
  gene?: string
  log2FC?: number
  pval?: number
  adj_pval?: number
  sig?: string
  neglog10_pval?: number
  type?: string
  tooltip_value?: string
}

interface Opts {
  pval_cutoff: number
  fc_cutoff: number
  width: number
  height: number
  xaxis: "log2FC"
  yaxis: "pval" | "adj_pval"
  xaxis_label: string
  yaxis_label: string
}

let tooltipTimeout: number

function distance(point1: [number, number], point2: [number, number]) {
  const dx = point2[0] - point1[0]
  const dy = point2[1] - point1[1]
  return Math.sqrt(dx * dx + dy * dy)
}

export default withTooltip<
  {
    data: Data[]
    opts: Opts
    width: number
    height: number
    setComponentValue: any
  },
  ToolTipData
>(
  ({
    data,
    opts,
    width,
    height,
    setComponentValue,
    showTooltip,
    hideTooltip,
    tooltipOpen,
    tooltipData,
    tooltipLeft,
    tooltipTop,
  }) => {
    // chart dimensions
    console.log(`width: ${width}, height: ${height}`)
    height = 300

    // margins
    const margin = { top: 10, right: 80, bottom: 50, left: 80 }

    // inner dimensions
    const innerWidth = width - margin.left - margin.right
    const innerHeight = height - margin.top - margin.bottom

    // accessor functions (for scales)
    const x = (d: Data) => d[opts.xaxis]
    const y = (d: Data) => d[opts.yaxis]
    const sig = (d: Data) => d.sig

    // create svg ref
    const svgRef = useRef<SVGSVGElement>(null)

    // neighbor radius
    const neighborRadius = 3

    // scales
    const xScale = scaleLinear({
      range: [margin.left, innerWidth + margin.left],
      domain: extent(data, x) as [number, number],
    })

    const yScale = scaleLinear({
      range: [innerHeight + margin.top, margin.top],
      domain: extent(data, y) as [number, number],
    })

    const colorScale = scaleOrdinal({
      domain: ["not significant", "upregulated", "downregulated"],
      range: ["gray", "red", "blue"],
    })

    // adjust cutoffs
    const pval_cutoff = -Math.log10(opts.pval_cutoff)
    const fc_cutoff = Math.log2(opts.fc_cutoff)

    // legend glyph size
    const legendSize = 15

    // event handlers
    const handleMouseMovePoint = useCallback(
      (event: React.MouseEvent | React.TouchEvent) => {
        if (tooltipTimeout) clearTimeout(tooltipTimeout)
        if (!svgRef.current) return

        // find nearest point to current mouse position
        const point = localPoint(svgRef.current, event)
        if (!point) return
        const closest = data.find(
          (d) =>
            distance([xScale(x(d)), yScale(y(d))], [point.x, point.y]) <=
            neighborRadius
        )
        if (closest) {
          closest.type = "point"
          showTooltip({
            tooltipLeft: xScale(x(closest)),
            tooltipTop: yScale(y(closest)),
            tooltipData: closest,
          })
        }
      },
      [xScale, yScale, showTooltip, data]
    )

    const handleMouseLeavePoint = useCallback(() => {
      tooltipTimeout = window.setTimeout(() => {
        hideTooltip()
      }, 200)
    }, [hideTooltip])

    return (
      <>
        <LegendOrdinal scale={colorScale} labelFormat={(label) => `${label}`}>
          {(labels) => (
            <div style={{ display: "flex", justifyContent: "center" }}>
              {labels.map((label, i) => (
                <LegendItem
                  key={`legend-quantile-${i}`}
                  margin="0 5px"
                  onClick={() => {
                    // TODO: Hide or show corresponding points
                    console.log(`clicked: ${JSON.stringify(label)}`)
                  }}
                >
                  <svg width={legendSize} height={legendSize}>
                    {/* <rect fill={label.value} width={legendSize} height={legendSize} /> */}
                    <circle
                      fill={label.value}
                      cx={legendSize / 2}
                      cy={legendSize / 2}
                      r={legendSize / 2}
                    />
                  </svg>
                  <LegendLabel align="center" margin="0 4px">
                    {label.text}
                  </LegendLabel>
                </LegendItem>
              ))}
            </div>
          )}
        </LegendOrdinal>

        <svg width={width} height={height} ref={svgRef}>
          <rect
            x={margin.left}
            y={margin.top}
            width={innerWidth}
            height={innerHeight}
            fill="transparent"
            onMouseMove={handleMouseMovePoint}
            onMouseLeave={handleMouseLeavePoint}
            onTouchMove={handleMouseMovePoint}
            onTouchEnd={handleMouseLeavePoint}
          />

          <AxisLeft
            scale={yScale}
            tickFormat={format(".2g")}
            left={margin.left}
            label={opts.yaxis_label}
            labelOffset={50}
            labelClassName="axis-label"
          />
          <Axis
            scale={xScale}
            orientation="bottom"
            top={innerHeight + margin.top}
            tickFormat={format(".2f")}
            label={opts.xaxis_label}
            labelClassName="axis-label"
            labelOffset={15}
          />

          <GridColumns
            top={margin.top}
            scale={xScale}
            height={innerHeight}
            strokeOpacity={1}
            pointerEvents="none"
          />
          <GridRows
            left={margin.left}
            scale={yScale}
            width={innerWidth}
            strokeOpacity={1}
            pointerEvents="none"
          />

          <Group>
            {data.map((d, i) => (
              <Circle
                key={`point-${i}`}
                cx={xScale(x(d))}
                cy={yScale(y(d))}
                r={3}
                fill={tooltipData === d ? "black" : colorScale(sig(d))}
                fillOpacity={0.5}
                onMouseMove={handleMouseMovePoint}
                onMouseLeave={handleMouseLeavePoint}
                onTouchMove={handleMouseMovePoint}
                onTouchEnd={handleMouseLeavePoint}
                onClick={() => setComponentValue(d)}
              />
            ))}
          </Group>

          <Line
            from={{ x: xScale(fc_cutoff), y: margin.top }}
            to={{ x: xScale(fc_cutoff), y: height - margin.bottom }}
            stroke="black"
            onMouseMove={(event) => {
              if (!svgRef.current) return
              const point = localPoint(svgRef.current, event)
              if (!point) return
              showTooltip({
                tooltipLeft: point.x,
                tooltipTop: point.y,
                tooltipData: {
                  type: "line",
                  tooltip_value: `${opts.fc_cutoff} fold change`,
                },
              })
            }}
            onMouseLeave={handleMouseLeavePoint}
          />
          <Line
            from={{ x: xScale(-fc_cutoff), y: margin.top }}
            to={{ x: xScale(-fc_cutoff), y: height - margin.bottom }}
            stroke="black"
            onMouseMove={(event) => {
              if (!svgRef.current) return
              const point = localPoint(svgRef.current, event)
              if (!point) return
              showTooltip({
                tooltipLeft: point.x,
                tooltipTop: point.y,
                tooltipData: {
                  type: "line",
                  tooltip_value: `${opts.fc_cutoff} fold change`,
                },
              })
            }}
            onMouseLeave={handleMouseLeavePoint}
          />
          <Line
            from={{ x: margin.left, y: yScale(pval_cutoff) }}
            to={{ x: width - margin.right, y: yScale(pval_cutoff) }}
            stroke="black"
            onMouseMove={(event) => {
              if (!svgRef.current) return
              const point = localPoint(svgRef.current, event)
              if (!point) return
              showTooltip({
                tooltipLeft: point.x,
                tooltipTop: point.y,
                tooltipData: {
                  type: "line",
                  tooltip_value: `${opts.pval_cutoff} p-value`,
                },
              })
            }}
            onMouseLeave={handleMouseLeavePoint}
          />
        </svg>
        {tooltipOpen &&
          tooltipData &&
          tooltipLeft != null &&
          tooltipTop != null && (
            <Tooltip left={tooltipLeft + 10} top={tooltipTop + 10}>
              {tooltipData.type === "line" && (
                <div>
                  <strong>Line: </strong>
                  {tooltipData.tooltip_value}
                </div>
              )}
              {tooltipData.type === "point" && (
                <div>
                  <strong>{tooltipData.probe}</strong>
                  <br />
                  <strong>{tooltipData.gene}</strong>
                  <br />
                  <strong>log2FC: </strong>
                  {tooltipData.log2FC}
                  <br />
                  <strong>p-val: </strong>
                  {tooltipData.pval}
                  <br />
                  <strong>adj p-val: </strong>
                  {tooltipData.adj_pval}
                </div>
              )}
            </Tooltip>
          )}
      </>
    )
  }
)
