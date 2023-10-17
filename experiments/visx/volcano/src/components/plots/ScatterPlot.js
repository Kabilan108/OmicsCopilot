
import React from "react";
import { useRef, useMemo, useCallback } from "react"

import { wbData } from "../../worldBankData.js"

import { scaleLinear, scaleLog, scaleSqrt, scaleOrdinal } from "@visx/scale";
import { extent, format } from "d3";
import { Circle } from "@visx/shape"
import { Group } from "@visx/group"
import { Axis, AxisLeft } from "@visx/axis"
import { GridColumns } from "@visx/grid"
import { LegendOrdinal } from "@visx/legend"
import ParentSize from "@visx/responsive/lib/components/ParentSize"
import { useTooltip, TooltipWithBounds, defaultStyles } from "@visx/tooltip"
import { localPoint } from "@visx/event"
import { voronoi } from "@visx/voronoi"


const ScatterPlot = ({
  data = wbData,
  width = 800,
  height = 500,
  margin = { top: 30, right: 60, bottom: 40, left: 40 },
}) => {
  // Define dimensions of chart
  const innerWidth = width - margin.left - margin.right;
  const innerHeight = height - margin.top - margin.bottom;

  // Create accessor functions
  const x = (d) => d.gdpPerCap;
  const y = (d) => d.lifeExpectancy;
  const radius = (d) => d.population;
  const color = (d) => d.region;  

  // Create scales
  const xScale = scaleLog({
    range: [margin.left, innerWidth + margin.left],
    domain: extent(data, x),  // extent returns min and max values of array
  })

  const yScale = scaleLinear({
    range: [innerHeight + margin.top, margin.top],
    domain: extent(data, y), // extent returns min and max values of array
  })

  const colorScale = scaleOrdinal({
    range: ["#ff8906", "#3da9fc", "#ef4565", "#7f5af0", "#2cb67d"],
    domain: [...new Set(data.map(color))],
  })

  const rScale = scaleSqrt({
    range: [3, 30],
    domain: extent(data, radius),
  })

  // Tooltip handlers
  const {
    showTooltip,
    hideTooltip,
    tooltipData,
    tooltipOpen,
    tooltipTop = 0,
    tooltipLeft = 0,
  } = useTooltip();

  // Create a voronoi diagram of the chart area
  // This allows us to find the closest point to hover position
  const voronoiLayout = useMemo(
    () =>
      voronoi({
        x: (d) => xScale(x(d)) ?? 0,
        y: (d) => yScale(y(d)) ?? 0,
        width,
        height,
      })(data),

    // Dependencies of voronoiLayout
    [data, width, height, xScale, yScale]
  )

  // Make tooltip transient and track state of svg
  let tooltipTimeout;
  const svgRef = useRef(null);

  // Define callback to show tooltip
  const handleMouseMove = useCallback(
    (event) => {
      if (tooltipTimeout) clearTimeout(tooltipTimeout);  // clear timeout if it exists
      if (!svgRef.current) return;  // if SVG not yet rendered, do nothing

      // Get coordinates of mouse pointer relative to SVG
      const point = localPoint(svgRef.current, event);

      if (!point) return; // if mouse pointer not in SVG, do nothing

      // find the nearest polygon to the current mouse position
      const neighborRadius = 10;  // radius of circle around mouse pointer to search for closest point
      const closest = voronoiLayout.find(point.x, point.y, neighborRadius);
      
      // Show tooltip if closest point found
      if (closest) {
        showTooltip({
          tooltipLeft: xScale(x(closest.data)),
          tooltipTop: yScale(y(closest.data)),
          tooltipData: closest.data,
        })
      }
    },
    
    // Dependencies of callback
    [xScale, yScale, showTooltip, voronoiLayout, tooltipTimeout]
  )

  // Callback for whe cursor leaves plot area
  const handleMouseLeave = useCallback(
    () => {
      tooltipTimeout = setTimeout(() => {
        hideTooltip();
      }, 1500);
    },
    [hideTooltip]
  )

  // Sort data so that smaller circles are drawn on top
  data = data.sort((a, b) => b.population - a.population)

  return (
    <>
      <LegendOrdinal
        scale={colorScale}
        direction="row"
        shape="circle"
        style={{
          display: "flex",
          justifyContent: "space-between",
        }}
      />

      <svg width={width} height={height} ref={svgRef}>
        {/* Fills dimensions of plot area and detects when mouse enters/leaves */}
        <rect 
          x={margin.left}
          y={margin.top}
          width={innerWidth}
          height={innerHeight}
          fill="transparent"
          onMouseMove={handleMouseMove}
          onMouseLeave={handleMouseLeave}
          onTouchMove={handleMouseMove}
          onTouchEnd={handleMouseLeave}
        />

        <AxisLeft scale={yScale} left={margin.left} label='Life expectancy' />
        <Axis
          orientation="top"
          scale={xScale}
          top={margin.top}
          tickFormat={format("$~s")}
          numTicks={2}
          tickStroke="transparent"
          stroke="transparent"
        />
        <Axis
          orientation="bottom"
          scale={xScale}
          top={innerHeight + margin.top}
          tickFormat={format("$~s")}
          numTicks={2}
          label="GDP per capita"
        />

        <GridColumns
          top={margin.top}
          scale={xScale}
          height={innerHeight}
          strokeOpacity={1}
          pointerEvents='none'
          numTicks={2}
        />

        <Group pointerEvents='none'>
          {data.map((point, i) => (
            <Circle
              key={i}
              cx={xScale(x(point))}
              cy={yScale(y(point))}
              r={rScale(radius(point))}
              fill={colorScale(color(point))}
              fillOpacity={0.8}
            />
          ))}
        </Group>
      </svg>

      {/* Add the tooltip and apply styles */}
      {tooltipOpen && tooltipData && tooltipLeft != null && tooltipTop != null && (
        <TooltipWithBounds
          left={tooltipLeft + 10}
          top={tooltipTop + 10}
          style={defaultStyles}
        >
          <h3
            style={{
              color: colorScale(color(tooltipData)),
              padding: 0,
              margin: 0,
            }}
          >
            {tooltipData.country}
          </h3>
          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gridTemplateRows: "1fr"
            }}
          >
            <div>GDP per cap</div>
            <div style={{ textAlign: "right" }}>
              { `${format("$.2~s")(x(tooltipData))}` }
            </div>

            <div>Life Expectancy</div>
            <div style={{ textAlign: "right" }}>
              { Math.round(y(tooltipData)) }
            </div>

            <div>Population</div>
            <div style={{ textAlign: "right" }}>
              { `${Math.round(radius(tooltipData))}m` }
            </div>
          </div>
        </TooltipWithBounds>
      )}

    </>
  );
}

const ScatterPlotWrapper = () => (
  <ParentSize>
    {({ width, height }) => <ScatterPlot width={width} height={height} />}
  </ParentSize>
)

export default ScatterPlotWrapper;
