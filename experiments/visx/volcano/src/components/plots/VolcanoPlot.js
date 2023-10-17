// // src/VolcanoPlot.js
// import React from 'react';
// import { scaleLinear } from '@visx/scale';
// import { Circle } from '@visx/shape';
// import { Group } from '@visx/group';
// import { AxisBottom, AxisLeft } from '@visx/axis';
// import { withTooltip, Tooltip, defaultStyles as defaultTooltipStyles } from '@visx/tooltip';
// import { WithTooltipProvidedProps } from '@visx/tooltip/lib/enhancers/withTooltip';

// const width = 800;
// const height = 500;
// const margin = { top: 20, right: 20, bottom: 50, left: 50 };

// interface tooltipData {
//    gene?: string;
//    probe?: string;
// }

// export default withTooltip(function VolcanoPlot({ data, tooltipOpen, tooltipData, showTooltip, hideTooltip }) {
//    const xScale = scaleLinear({
//       domain: [Math.min(...data.map(d => d["log2(FC)"])), Math.max(...data.map(d => d["log2(FC)"]))],
//       range: [margin.left, width - margin.right],
//    });
//    const yScale = scaleLinear({
//       domain: [0, Math.max(...data.map(d => d["-log10(adj_pvalue)"]))],
//       range: [height - margin.bottom, margin.top],
//    });

//    return (
//       <svg width={width} height={height}>
//          <Group>
//             {data.map((d, i) => (
//                <Circle
//                   key={i}
//                   cx={xScale(d["log2(FC)"])}
//                   cy={yScale(d["-log10(adj_pvalue)"])}
//                   r={5}
//                   onMouseOver={() => showTooltip({
//                      tooltipData: { gene: d.gene, probe: d.probe },
//                   })}
//                   onMouseOut={hideTooltip}
//                />
//             ))}
//             <AxisBottom
//                scale={xScale}
//                top={height - margin.bottom}
//                label="$log_{2}\left( \text{Fold change} \right)$"
//                labelProps={{
//                   fill: '#000',
//                   textAnchor: 'middle',
//                   fontSize: 12,
//                   fontFamily: 'Arial',
//                }}
//             />
//             <AxisLeft
//                scale={yScale}
//                left={margin.left}
//                label="$log_{10}\left( \text{Adjusted p-value} \right)$"
//                labelProps={{
//                   fill: '#000',
//                   textAnchor: 'middle',
//                   fontSize: 12,
//                   fontFamily: 'Arial',
//                }}
//             />
//          </Group>
//          {tooltipOpen && (
//             <Tooltip
//                top={yScale(tooltipData["-log10(adj_pvalue)"])}
//                left={xScale(tooltipData["log2(FC)"])}
//                style={defaultTooltipStyles}
//             >
//                <div>
//                   <strong>{tooltipData.gene}</strong>
//                   <p>{tooltipData.probe}</p>
//                </div>
//             </Tooltip>
//          )}
//       </svg>
//    );
// });

