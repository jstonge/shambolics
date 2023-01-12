// export function plot_diamond(dat) {
  
//     const max_xy   = d3.max(dat, d => d.x1)           // max_x == max_y
//     const max_rank = d3.max(dat, (d) => d.rank_L[1]); // max_rankL == max_rankL
//     const max_val  = d3.max(dat, d => d.value)
  
//     const xy         = d3.scaleBand().domain(dat.map(d=>d.y1)).range([0, visWidth])
//     const xyDomain   = [1, 10**Math.ceil(Math.max(Math.log10(max_rank)))];
//     const xyScale    = d3.scaleLog().domain(xyDomain).range([1, visWidth])
//     const xyScaleLin = d3.scaleLinear().domain([1,ncells]).range([1, visWidth])
    
//     const color_scale = d3.scaleSequentialLog().domain([max_val, 1]).interpolator(d3.interpolateInferno)
    
//     const svg = d3.select(DOM.svg(visWidth + margin.top, visHeight))
    
//     const g = svg.attr("id", "myGraph")   
//       .attr('height', visHeight + margin.top + margin.bottom)
//       .attr('width', visWidth)
//       .append('g');
    
//     // Rotate the canvas
//     svg.attr('transform', `translate(${ visWidth / 2.5 }, -25) rotate(135) scale(1,-1)`);
  
//     // Xaxis 
//     g.append('g')
//       .call(xAxis, xyScale)
//       .call(xAxisLab, "Rank r", visWidth, 40) // there must be an easier way to breaklines!?!
//       .call(xAxisLab, "for", visWidth, 60)
//       .call(xAxisLab, `${title(1)}`, visWidth, 80)
//       .call(xAxisLab, "more →", visWidth-200, 40, .4)
//       .call(xAxisLab, "frequent", visWidth-200, 60, .4)
//       .call(xAxisLab, "← less", visWidth+200, 40, .4)
//       .call(xAxisLab, "frequent", visWidth+200, 60, .4)
//       .call(xGrid, xyScaleLin);
    
//     // Yaxis 
//     g.append('g')
//       .call(yAxis, xyScale)
//       .call(yAxisLab, "Rank r", 0, 40)
//       .call(yAxisLab, "for", 0, 60)
//       .call(yAxisLab, `${title(0)}`, 0, 80)
//       .call(yAxisLab, "less →", 200, 40, .4)
//       .call(yAxisLab, "frequent", 200, 60, .4)
//       .call(yAxisLab, "← more", -200, 40, .4)
//       .call(yAxisLab, "frequent", -200, 60, .4)
//       .call(yGrid, xyScaleLin);
    
//     // Background polygons
//     function draw_polygon(g, tri_coords, bg_color) {
//        g.append("polygon")
//           .attr("fill",bg_color)
//           .attr("fill-opacity", 0.2)
//           .attr("stroke", "black")
//           .attr("stroke-width", 1)
//           .attr("points", tri_coords)
//      }
    
//     const grey_triangle = [
//       {"x":max_xy, "y":max_xy}, {"x":0, "y":0}, {"x":max_xy, "y":0}
//     ].map(d => [xy(d.x), xy(d.y)].join(',')).join(" ")
    
//     const blue_triangle = [
//       {"x":max_xy, "y":max_xy}, {"x":0, "y":0}, {"x":0, "y":max_xy}
//     ].map(d => [xy(d.x), xy(d.y)].join(',')).join(" ")
    
//     draw_polygon(g, blue_triangle, "#89CFF0")
//     draw_polygon(g, grey_triangle, "grey")
        
//     // Heatmap
//     const base_hm = g.selectAll('rect').data(dat).enter();
    
//     const cells = base_hm
//       .append('rect')
//         .attr('x', (d) => xy(d.x1))
//         .attr('y', (d) => xy(d.y1))
//         .attr('width', xy.bandwidth())
//         .attr('height', xy.bandwidth())
//         .attr('fill', (d) => color_scale(d.value))
//         .attr('fill-opacity', (d) => d.value === 0 ? 0 : color_scale(d.value))
//         .attr('stroke', 'black')
//         .attr('stroke-width', (d) => d.value === 0 ? 0 : 0.3)
    
//     if (toggle_lab) {
//       svg.selectAll('text')
//       .data(dat)
//       .enter()
//       .append('text')
//       .filter(d => utils.rin(chosen_types, d.types.split(",")).some((x) => x === true))
//       .text(d => d.types.split(",")[0])
//         .attr("x", (d) => xy(d.x1))
//         .attr("y", (d) => Number.isInteger(d.coord_on_diag) ? xy(d.y1) : xy(d.y1)-1) // avoid text occlusion
//         .attr("dy", 20)
//         .attr("font-size", 14)
//         .attr("transform", d => `scale(1,-1) rotate(-90) rotate(-45, ${xy(d.x1)}, ${xy(d.y1)}) translate(${d.which_sys === "right" ? xy(Math.sqrt(d.cos_dist))*1.5 : -xy(Math.sqrt(d.cos_dist))*1.5}, 0)`) // little humph
//         .attr("text-anchor", d => d.x1 - d.y1 <= 0 ? "start" : "end")
//       }
    
//       // Draw the middle line
//       svg.append('line')
//        .style("stroke", "black")
//        .style("stroke-width", 1)
//        .attr("x1", 0)
//        .attr("y1", 0)
//        .attr("x2", visWidth-7)
//        .attr("y2", visHeight-7)
  
//     // Add the tooltip
//     const tooltip = d3
//       .select("body")
//       .append("div")
//       .style("position", "absolute")
//       .style("visibility", "hidden")
//       .style("opacity", 0.9)
//       .style("background", "white");
    
//     cells.call(Tooltips, tooltip) // not working with labels
    
//     return svg.node()
  
    
//   }

//   xAxis = (g, scale) =>
//   g
//     .attr("transform", `translate(0, ${visHeight})`)
//     .call(d3.axisBottom(scale))
//     .call((g) => g.select(".domain").remove()) // remove baseline
//     // add label
//     .selectAll('text')
//     .attr('dy', 10)
//     .attr('dx', 13)
//     .attr('transform', 'scale(-1,1) rotate(45)')
//     .attr('font-size', 10)
  
// xAxisLab = (g, text, dx, dy, alpha) =>
//     g
//       .append("text")
//       .attr("x", visWidth / 2)
//       .attr("fill", "black")
//       .attr("font-size", 14)
//       .attr("opacity", alpha)
//       .attr("text-anchor", 'middle')
//       .text(text)
//       .attr('transform', `rotate(183) scale(1,-1) translate(-${dx}, ${dy})`)

// xGrid = (g, scale) =>
//   g.append('g')
//     .attr("transform", `translate(-10, 0)`)
//     .call(d3.axisBottom(scale).ticks(ncells/2).tickFormat("")) // rm tick values
//     .call((g) => g.select(".domain").remove())
//     .call((g) =>
//       g
//         .selectAll(".tick line")
//         .attr("stroke", "#d3d3d3")
//           .style("stroke-dasharray", ("3, 3"))
//         .attr("y1", -visHeight)
//         .attr("y2", 0)
//     )

// yAxis = (g, scale) =>
//   // add axis
//   g
//     .call(d3.axisRight(scale))
//     .call((g) => g.select(".domain").remove())
//     .attr("transform", `translate(${visHeight+5}, 0) scale(-1, 1)`)
//     .selectAll('text')
//     .attr('dx', -28)
//     .attr('dy', 15)
//     .attr('transform', 'rotate(45)')
//     .attr('font-size', 10)

// yAxisLab = (g, text, dx, dy, alpha) =>
//     g
//       .append("text")
//       .attr("x", visWidth / 2)
//       .attr("fill", "black")
//       .attr("font-size", 14)
//       .attr("opacity", alpha)
//       .attr("text-anchor", 'middle')
//       .text(text)
//       .attr('transform', `rotate(93) translate(${dx},${dy})`)

//  yGrid = (g, scale) =>
//     g
//       .append("g")
//       .attr("transform", `translate(${visHeight+20}, -10) scale(-1, 1)`)
//       .call(d3.axisRight(scale).ticks(ncells/2).tickFormat(""))
//       .call((g) => g.select(".domain").remove())
//       .call((g) =>
//         g
//           .selectAll(".tick line")
//           .attr("stroke", "#d3d3d3")
//           .style("stroke-dasharray", ("3, 3"))
//           .attr("x1", 0)
//           .attr("x2", visWidth)
//       )