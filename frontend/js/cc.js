// Linked scatterplot module for covid communities
// Copyright (C) Oliver Davis 2020

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version. See https://www.gnu.org/licenses/

const cc = (function(d3){

  // Get diverging colour palette for unmet need
  function getColourScale(values){
    let xcs = d3.extent(values);
    // ColorBrewer palette, interpolation in LAB for perceptual constancy
    let colourScale = d3.scaleLinear()
      .domain([xcs[0],
        d3.mean(values),
        xcs[1]])
      // .range(["#4575b4","#ffffbf","#d73027"])
      // .range(["#001d95","#f0f0f0","#c32b38"])
      // .range(["#3781ff","#ffffbf","#c32b38"])
      // .range(["#3781ff","#f0f0f0","#c32b38"])
      // .range(["#225fb3","#f0f0f0","#dd1661"])
      .range(["#225fb3","#ffffef","#dd1661"])
      // .range(["#2166ac","#f7f7f7","#b2182b"])
      // .interpolate(d3.interpolateHcl);
      .interpolate(d3.interpolateLab);
    return colourScale;
  }

  // Return closure function to make sidebar toggle button
  // Button svg has id open_close for styling
  function getToggleAdder(){
    let open = true;
    function addToggle(sidebarSelector, sidebarWidth){
      const sidebar = d3.select(sidebarSelector);
      const open_close = sidebar.append("svg").attr("id","open_close");
      open_close.append("circle").attr("id", "opener").attr("cx", 20).attr("cy", 20).attr("r", 20).attr("fill", "#fff").attr("opacity", 0.5).style("cursor", "pointer");
      const cross_lines = open_close.append("g").attr("class", "cross_lines").style("pointer-events", "none");
      cross_lines.append("path").attr("d", "M 20 10 V 30").attr("stroke", "#4c4c4c").attr("stroke-width", 4).attr("stroke-linecap", "round");
      cross_lines.append("path").attr("d", "M 10 20 H 30").attr("stroke", "#4c4c4c").attr("stroke-width", 4).attr("stroke-linecap", "round");
      open_close.style("transform", "rotate(-45deg)");

      d3.select("#opener").on("click", e => {
        if(open){
          sidebar.transition().duration(750).style("right", "-" + sidebarWidth + "px");
          open_close.transition().duration(750).style("transform", "rotate(90deg)");
          open = false;
        } else {
          sidebar.transition().duration(750).style("right", "0px");
          open_close.transition().duration(750).style("transform", "rotate(-45deg)");
          open = true;
        }
      });
    }
    return addToggle;
  }

  // Calculate z score
  function z_score(d, mean, sd){
    return (d - mean)/sd;
  }

  // Calculate sum of z scores for composite measures
  function sumOfZ(vars, data, output_name){
    let means = {};
    let sds = {};
    vars.forEach(element => {
      means[element] = d3.mean(data, d => d[element]);
      sds[element] = d3.deviation(data, d => d[element]);
    });
    console.log(means);
    console.log(sds);
    data.forEach(element => {
      element.z_scores = [];
      vars.forEach((item, idx) => {
        element.z_scores[idx] = cc.z_score(element[item], means[item], sds[item]);
      });
      element.sum_of_z = element.z_scores.reduce((acc, cur) => {return (acc + cur);});
    });
    let mean_z = d3.mean(data, d => d.sum_of_z);
    let sd_z = d3.deviation(data, d => d.sum_of_z);
    data.forEach(element => {
      element[output_name] = cc.z_score(element.sum_of_z, mean_z, sd_z);
      delete element.sum_of_z;
      delete element.z_scores;
    });
    return data;
  }

  // Add the scatter plot
  function drawScatterplot(plotAreaId, x_var, y_var, data, height, width, margin, map, boundaries){
    const svg = d3.select(plotAreaId).append("g").attr("id", "plot");

    // Set the x and y scales
    let x = d3.scaleLinear()
      .domain(d3.extent(data, d => d[x_var])).nice()
      .range([margin.left, width - margin.right]);

    let y = d3.scaleLinear()
      .domain(d3.extent(data, d => d[y_var])).nice()
      .range([height - margin.bottom, margin.top]);

    // Mean of x and y
    let mean_x = d3.mean(data, d => d[x_var]);
    let mean_y = d3.mean(data, d => d[y_var]);

    // Standard deviation of x and y
    let sd_x = d3.deviation(data, d => d[x_var]);
    let sd_y = d3.deviation(data, d => d[y_var]);

    // Colour scale
    let colour_scale_values = data.map(
      d => {
        let zx = cc.z_score(d[x_var], mean_x, sd_x);
        let zy = cc.z_score(d[y_var], mean_y, sd_y);
        return zx - zy;
      }
    );

    let risk_colour = cc.getColourScale(colour_scale_values);

    // Linear regression
    let linearRegression = d3.regressionLinear()
      .x(d => d[x_var])
      .y(d => d[y_var]);

    let regression_summary = linearRegression(data);

    // Axis functions
    xAxis = g => g
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).ticks(width / 80))
      .style("font-family", "Lato,'Helvetica Neue',Arial,Helvetica,sans-serif")
      .style("font-size", "12px")
      .call(g => g.select(".domain").remove())
      .call(g => g.append("text")
        .style("font-family", "Lato,'Helvetica Neue',Arial,Helvetica,sans-serif")
        .style("font-size", "14px")
        .attr("x", width-2)
        .attr("y", margin.bottom)
        .attr("fill", "#000")
        .attr("text-anchor", "end")
        .text("Community need →")
        .attr("fill", "#dd1661")
      )

    yAxis = g => g
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(y))
      .style("font-family", "Lato,'Helvetica Neue',Arial,Helvetica,sans-serif")
      .style("font-size", "12px")
      .call(g => g.select(".domain").remove())
      .call(g => g.append("text")
        .style("font-family", "Lato,'Helvetica Neue',Arial,Helvetica,sans-serif")
        .style("font-size", "14px")
        .attr("x", -margin.left)
        .attr("y", 10)
        .attr("fill", "#000")
        .attr("text-anchor", "start")
        .text("↑ Community support")
        .attr("fill", "#225fb3")
      )

    // Grid function
    grid = g => g
      .attr("stroke", "currentColor")
      .attr("stroke-opacity", 0.1)
      .call(g => g.append("g")
        .selectAll("line")
        .data(x.ticks())
        .join("line")
          .attr("x1", d => 0.5 + x(d))
          .attr("x2", d => 0.5 + x(d))
          .attr("y1", margin.top)
          .attr("y2", height - margin.bottom))
      .call(g => g.append("g")
        .selectAll("line")
        .data(y.ticks())
        .join("line")
          .attr("y1", d => 0.5 + y(d))
          .attr("y2", d => 0.5 + y(d))
          .attr("x1", margin.left)
          .attr("x2", width - margin.right));

    // Mean of x
    const mean_x_base = height - margin.bottom - margin.top;
    const mean_x_place = x(mean_x);
    mark_mean_x = g => g
      .attr("transform", `translate(${mean_x_place},${margin.top})`)
      .append("path").attr("d",`M 0 0 L 0 ${mean_x_base}`)
      .attr("stroke","#333")
      .attr("shape-rendering", "crispEdges");

    // Mean of y
    const mean_y_base = width - margin.left - margin.right;
    const mean_y_place = y(mean_y);
    mark_mean_y = g => g
      .attr("transform", `translate(${margin.left},${mean_y_place})`)
      .append("path").attr("d",`M 0 0 L ${mean_y_base} 0`)
      .attr("stroke","#333")
      .attr("shape-rendering", "crispEdges");

    // Regression line
    const line = d3.line().x(d => x(d[0])).y(d => y(d[1]));
    const regression_line = line(regression_summary);
    draw_regression_line = g => g
      .append("path").attr("d",regression_line)
      .attr("stroke","#aaa")
      .attr("shape-rendering", "geometricPrecision");

    // Plot axes
    svg.append("g")
      .call(xAxis);

    svg.append("g")
      .call(yAxis);

    // Plot grid
    svg.append("g")
      .call(grid);

    // Plot mean of x
    svg.append("g")
      .call(mark_mean_x);

    // Plot mean of y
    svg.append("g")
      .call(mark_mean_y);

    // Plot regression line
    svg.append("g")
      .call(draw_regression_line);

    // Assign colours
    data.forEach(d => d.colour = risk_colour(
      (cc.z_score(d[x_var], mean_x, sd_x) - cc.z_score(d[y_var], mean_y, sd_y))
    ));

    boundaries.features.forEach(d => {
      let matching_data = data.find(
        element => {return element.lad19cd === d.properties.lad18cd}
      );
      d.properties.colour = matching_data.colour;
    });
    map.getSource('boundaries_LAs').setData(boundaries);

    // Remember the latest linked map area
    let linkedArea = null;

    // Mouse event handlers for graph
    function handleMouseOver(d, i){
      d3.select(this).transition().duration(50).attr("r", 12).attr("stroke-width", 2);
      linkedArea = map.querySourceFeatures("boundaries_LAs",{
        filter: ["==",["get","lad18cd"], d.lad19cd]
      })[0].id;
      map.setFeatureState(
        {source: "boundaries_LAs", id: linkedArea},
        {hover: true}
      );
    }

    function handleMouseOut(d, i){
      d3.select(this).transition().duration(50).attr("r", 7).attr("stroke-width", 1.5);
      map.setFeatureState(
        {source: "boundaries_LAs", id: linkedArea},
        {hover: false}
      );
      linkedArea = null;
    }

    // Graph data points
    svg.append("g")
      .attr("stroke", "#505050")
      .attr("stroke-width", 1.5)
    .selectAll("circle")
      .data(data)
      .join("circle")
      .attr("id", d => d.lad19cd)
      .attr("class", "datapoints")
      .attr("cx", d => x(d[x_var]))
      .attr("cy", d => y(d[y_var]))
      .attr("r", 7)
      .attr("fill", d => d.colour)
      .on("mouseover", handleMouseOver)
      .on("mouseout", handleMouseOut);

  } // End draw scatterplot

  // Add the beeswarm plot
  function drawBeeswarm(plotAreaId, x_var, data, height, width, margin, map, boundaries){
    const svg = d3.select(plotAreaId).append("g").attr("id", "plot");

    // Set the x scale
    let x = d3.scaleLinear()
      .domain(d3.extent(data, d => d[x_var])).nice()
      .range([margin.left, width - margin.right]);

    // Mean of x
    let mean_x = d3.mean(data, d => d[x_var]);

    // Standard deviation of x
    let sd_x = d3.deviation(data, d => d[x_var]);

    // Colour scale
    let colour_scale_values = data.map(
      d => {
        let zx = cc.z_score(d[x_var], mean_x, sd_x);
        return zx;
      }
    );

    let risk_colour = cc.getColourScale(colour_scale_values);

    // Axis function
    xAxis = g => g
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).ticks(width / 80))
      .style("font-family", "Lato,'Helvetica Neue',Arial,Helvetica,sans-serif")
      .style("font-size", "12px")
      .call(g => g.select(".domain").remove())
      .call(g => g.append("text")
      .style("font-family", "Lato,'Helvetica Neue',Arial,Helvetica,sans-serif")
      .style("font-size", "14px")
        .attr("x", width - 2)
        .attr("y", margin.bottom)
        .attr("fill", "#000")
        .attr("text-anchor", "end")
        .text("Selected measure →"))

    // Grid function
    grid = g => g
      .attr("stroke", "currentColor")
      .attr("stroke-opacity", 0.1)
      .call(g => g.append("g")
        .selectAll("line")
        .data(x.ticks())
        .join("line")
          .attr("x1", d => 0.5 + x(d))
          .attr("x2", d => 0.5 + x(d))
          .attr("y1", margin.top)
          .attr("y2", height - margin.bottom));
      // .call(g => g.append("g")
      //   .append("line")
      //     .attr("y1", height - margin.bottom)
      //     .attr("y2", height - margin.bottom)
      //     .attr("x1", margin.left)
      //     .attr("x2", width - margin.right))
      // .call(g => g.append("g")
      //   .append("line")
      //     .attr("y1", margin.top)
      //     .attr("y2", margin.top)
      //     .attr("x1", margin.left)
      //     .attr("x2", width - margin.right));

    // Mean of x
    const mean_x_base = height - margin.bottom - margin.top;
    const mean_x_place = x(mean_x);
    mark_mean_x = g => g
      .attr("transform", `translate(${mean_x_place},${margin.top})`)
      .append("path").attr("d",`M 0 0 L 0 ${mean_x_base}`)
      .attr("stroke","#333")
      .attr("shape-rendering", "crispEdges");

    // Plot axis
    svg.append("g")
      .call(xAxis);

    // Plot grid
    svg.append("g")
      .call(grid);

    // Plot mean of x
    svg.append("g")
      .call(mark_mean_x);

    // Assign colours
    data.forEach(d => d.colour = risk_colour(
      cc.z_score(d[x_var], mean_x, sd_x)
    ));

    boundaries.features.forEach(d => {
      let matching_data = data.find(
        element => {return element.lad19cd === d.properties.lad18cd}
      );
      d.properties.colour = matching_data.colour;
    });
    map.getSource('boundaries_LAs').setData(boundaries);

    // Remember the latest linked map area
    let linkedArea = null;

    // Mouse event handlers for graph
    function handleMouseOver(d, i){
      d3.select(this).transition().duration(50).attr("r", 12).attr("stroke-width", 2);
      linkedArea = map.querySourceFeatures("boundaries_LAs",{
        filter: ["==",["get","lad18cd"], d.lad19cd]
      })[0].id;
      map.setFeatureState(
        {source: "boundaries_LAs", id: linkedArea},
        {hover: true}
      );
    }

    function handleMouseOut(d, i){
      d3.select(this).transition().duration(50).attr("r", 7).attr("stroke-width", 1.5);
      map.setFeatureState(
        {source: "boundaries_LAs", id: linkedArea},
        {hover: false}
      );
      linkedArea = null;
    }

    const simulation = d3.forceSimulation(data)
      .force("x", d3.forceX(function(d) { return x(d[x_var]); }).strength(5))
      .force("y", d3.forceY(height / 2))
      .force("collide", d3.forceCollide(10))
      .stop();

    for (var i = 0; i < 120; ++i) simulation.tick();

    // Graph data points
    svg.append("g")
      .attr("stroke", "#505050")
      .attr("stroke-width", 1.5)
    .selectAll("circle")
      .data(data)
      .join("circle")
      .attr("id", d => d.lad19cd)
      .attr("class", "datapoints")
      .attr("cx", d => d.x)
      .attr("cy", d => d.y)
      .attr("r", 7)
      .attr("fill", d => d.colour)
      .on("mouseover", handleMouseOver)
      .on("mouseout", handleMouseOut);
  } // end drawBeeswarm

  // Calculate variables and redraw plot, recolour map
  function redraw(plotAreaId, chosen_supports, chosen_needs, data, height, width, margin, map, boundaries){
    d3.select("#plot").remove();
    let x_var, y_var, supports_var = null, needs_var = null;
    if(chosen_supports.length === 1){
      supports_var = chosen_supports[0];
    } else if(chosen_supports.length > 1){
      data = cc.sumOfZ(chosen_supports, data, "supports_composite");
      supports_var = "supports_composite";
    }
    if(chosen_needs.length === 1){
      needs_var = chosen_needs[0];
    } else if(chosen_needs.length > 1){
      data = cc.sumOfZ(chosen_needs, data, "needs_composite");
      needs_var = "needs_composite";
    }
    if(needs_var !== null){
      x_var = needs_var;
      if(supports_var !== null){
        y_var = supports_var;
        // scatterplot
        cc.drawScatterplot(plotAreaId, x_var, y_var, data, height, width, margin, map, boundaries);
      } else {
        // beeswarm
        cc.drawBeeswarm(plotAreaId, x_var, data, height, width, margin, map, boundaries);
      }
    } else if(supports_var !== null){
      x_var = supports_var;
      // beeswarm
      cc.drawBeeswarm(plotAreaId, x_var, data, height, width, margin, map, boundaries);
    } else {
      console.log("No variables selected");
      boundaries.features.forEach(d => {
        d.properties.colour = "#ffffff";
      });
      map.getSource('boundaries_LAs').setData(boundaries);
    }
  }

  return {
    drawScatterplot: drawScatterplot,
    drawBeeswarm: drawBeeswarm,
    redraw: redraw,
    getColourScale: getColourScale,
    getToggleAdder: getToggleAdder,
    z_score: z_score,
    sumOfZ: sumOfZ
  };
})(d3);
