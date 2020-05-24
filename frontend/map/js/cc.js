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

  function getColourScale_need(values){
    let xcs = d3.extent(values);
    // ColorBrewer palette, interpolation in LAB for perceptual constancy
    let colourScale = d3.scaleLinear()
      .domain([xcs[0],
        xcs[1]])
      .range(["#ffffef","#dd1661"])
      .interpolate(d3.interpolateLab);
    return colourScale;
  }

  function getColourScale_support(values){
    let xcs = d3.extent(values);
    // ColorBrewer palette, interpolation in LAB for perceptual constancy
    let colourScale = d3.scaleLinear()
      .domain([xcs[0],
        xcs[1]])
      .range(["#ffffef","#225fb3"])
      .interpolate(d3.interpolateLab);
    return colourScale;
  }

  // Return closure function to make sidebar toggle button
  // Button svg has id open_close for styling
  function getToggleAdder(){
    let open = true;
    function addToggle(sidebarSelector, pageContentSelector, sidebarWidth){
      hiddenWidth = sidebarWidth + 100;
      const sidebar = d3.select(sidebarSelector);
      const page_contents = d3.select(pageContentSelector);
      const open_close = page_contents.append("svg").attr("id","open_close");
      open_close.append("circle").attr("id", "opener").attr("cx", 20).attr("cy", 20).attr("r", 20).attr("fill", "#fff").attr("opacity", 0.5).style("cursor", "pointer");
      const cross_lines = open_close.append("g").attr("class", "cross_lines").style("pointer-events", "none");
      cross_lines.append("path").attr("d", "M 20 10 V 30").attr("stroke", "#4c4c4c").attr("stroke-width", 4).attr("stroke-linecap", "round");
      cross_lines.append("path").attr("d", "M 10 20 H 30").attr("stroke", "#4c4c4c").attr("stroke-width", 4).attr("stroke-linecap", "round");
      open_close.style("transform", "rotate(-45deg)");

      d3.select("#opener").on("click", e => {
        if(open){
          sidebar.transition().duration(750).style("right", "-" + hiddenWidth + "px");
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
  function drawScatterplot(plotAreaId, x_var, y_var, data, height, width, margin, map, boundaries, boundaries_source){

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
      .call(d3.axisBottom(x).ticks(width / 80).tickFormat(d3.format(".2s")))
      .style("font-family", "Lato,'Helvetica Neue',Arial,Helvetica,sans-serif")
      .style("font-size", "12px")
      // .call(g => g.select(".domain").remove())
      // .call(g => g.append("text")
      //   .style("font-family", "Lato,'Helvetica Neue',Arial,Helvetica,sans-serif")
      //   .style("font-size", "14px")
      //   .attr("x", width-2)
      //   .attr("y", margin.bottom)
      //   .attr("fill", "#000")
        // .attr("text-anchor", "end")
        // .text("Community need →")
        // .attr("fill", "#dd1661")
      // )

    yAxis = g => g
      .attr("transform", `translate(${margin.left},0)`)
      .call(d3.axisLeft(y).tickFormat(d3.format(".2s")))
      .style("font-family", "Lato,'Helvetica Neue',Arial,Helvetica,sans-serif")
      .style("font-size", "12px")
      // .call(g => g.select(".domain").remove())
      // .call(g => g.append("text")
      //   .style("font-family", "Lato,'Helvetica Neue',Arial,Helvetica,sans-serif")
      //   .style("font-size", "14px")
      //   .attr("x", -margin.left)
      //   .attr("y", 10)
      //   .attr("fill", "#000")
      //   // .attr("text-anchor", "start")
      //   // .text("↑ Community support")
      //   // .attr("fill", "#225fb3")
      // )

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
        element => {return element.areaID === d.properties[element.mapID]}
      );
      d.properties.colour = matching_data.colour;
    });
    map.getSource(boundaries_source).setData(boundaries);

    // Remember the latest linked map area
    let linkedArea = null;

    // Mouse event handlers for graph
    function handleMouseOver(d, i){
      let this_circle = d3.select(this);
      this_circle.transition().duration(50).attr("r", "12").attr("stroke-width", 2);

      let x = this_circle.attr("cx");
      let y = this_circle.attr("cy");

      let tooltip_text = d.areaName;
      let tooltip_width = (tooltip_text.length * 8) + 14;

      let tooltip = d3.select(".cc_tooltip");
      tooltip.html(tooltip_text)
        .style("width", tooltip_width + "px")
        .style("left", ((x - tooltip_width) + 15) + "px")
        .style("top", (y - 45) + "px");
      tooltip.transition().duration(50).style("opacity", 0.8);

      linkedArea = map.querySourceFeatures(boundaries_source,{
        filter: ["==",["get", d.mapID], d.areaID]
      })[0].id;
      map.setFeatureState(
        {source: boundaries_source, id: linkedArea},
        {hover: true}
      );
    }

    function handleMouseOut(d, i){
      d3.select(this).transition().duration(50).attr("r", d => d.circleSize).attr("stroke-width", 1.5);
      map.setFeatureState(
        {source: boundaries_source, id: linkedArea},
        {hover: false}
      );
      linkedArea = null;

      let tooltip = d3.select(".cc_tooltip");
      tooltip.transition().duration(50).style("opacity", 0);
    }

    if(data.length < 100){

      // Graph data points
      svg.append("g")
        .attr("stroke", "#505050")
        .attr("stroke-width", 1.5)
      .selectAll("circle")
        .data(data)
        .join("circle")
        .attr("id", d => d.areaID)
        .attr("class", "datapoints")
        .attr("cx", d => x(d[x_var]))
        .attr("cy", d => y(d[y_var]))
        .attr("r", d => d.circleSize)
        .attr("fill", d => d.colour)
        .on("mouseover", handleMouseOver)
        .on("mouseout", handleMouseOut);

    } else {

      // Graph data points
      svg.append("g")
        .attr("stroke", "#505050")
        .attr("stroke-width", 0.25)
      .selectAll("circle")
        .data(data)
        .join("circle")
        .attr("id", d => d.areaID)
        .attr("class", "datapoints")
        .attr("cx", d => x(d[x_var]))
        .attr("cy", d => y(d[y_var]))
        .attr("r", d => d.circleSize)
        .attr("fill", d => d.colour)

    }

  } // End draw scatterplot

  // Add the beeswarm plot
  function drawBeeswarm(plotAreaId, x_var, data, height, width, margin, map, boundaries, boundaries_source, variable_class){

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

    // let risk_colour = cc.getColourScale(colour_scale_values);
    let risk_colour, axis_colour, axis_text;
    if(variable_class == "support"){
      risk_colour = cc.getColourScale_support(colour_scale_values);
      axis_colour = "#225fb3";
      axis_text = "Community support →";
    } else if(variable_class == "need"){
      risk_colour = cc.getColourScale_need(colour_scale_values);
      axis_colour = "#dd1661";
      axis_text = "Community need →";
    } else {
      risk_colour = cc.getColourScale(colour_scale_values);
      axis_colour = "#000000";
      axis_text = "Selected measure →";
    }

    // Axis function
    xAxis = g => g
      .attr("transform", `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).ticks(width / 80).tickFormat(d3.format(".2s")))
      .style("font-family", "Lato,'Helvetica Neue',Arial,Helvetica,sans-serif")
      .style("font-size", "12px")
      // .call(g => g.select(".domain").remove())
      // .call(g => g.append("text")
      // .style("font-family", "Lato,'Helvetica Neue',Arial,Helvetica,sans-serif")
      // .style("font-size", "14px")
      //   .attr("x", width - 2)
      //   .attr("y", margin.bottom)
      //   .attr("fill", "#000")
      //   // .attr("text-anchor", "end")
      //   // .text(axis_text)
      //   // .attr("fill", axis_colour))

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
        element => {return element.areaID === d.properties[element.mapID]}
      );
      d.properties.colour = matching_data.colour;
    });
    map.getSource(boundaries_source).setData(boundaries);

    // Remember the latest linked map area
    let linkedArea = null;

    // Mouse event handlers for graph
    function handleMouseOver(d, i){
      let this_circle = d3.select(this);
      this_circle.transition().duration(50).attr("r", "12").attr("stroke-width", 2);

      let x = this_circle.attr("cx");
      let y = this_circle.attr("cy");

      let tooltip_text = d.areaName;
      let tooltip_width = (tooltip_text.length * 8) + 14;

      let tooltip = d3.select(".cc_tooltip");
      tooltip.html(tooltip_text)
        .style("width", tooltip_width + "px")
        .style("left", ((x - tooltip_width) + 15) + "px")
        .style("top", (y - 45) + "px");
      tooltip.transition().duration(50).style("opacity", 0.8);

      linkedArea = map.querySourceFeatures(boundaries_source,{
        filter: ["==",["get", d.mapID], d.areaID]
      })[0].id;
      map.setFeatureState(
        {source: boundaries_source, id: linkedArea},
        {hover: true}
      );
    }

    function handleMouseOut(d, i){
      d3.select(this).transition().duration(50).attr("r", d => d.circleSize).attr("stroke-width", 1.5);
      map.setFeatureState(
        {source: boundaries_source, id: linkedArea},
        {hover: false}
      );
      linkedArea = null;

      let tooltip = d3.select(".cc_tooltip");
      tooltip.transition().duration(50).style("opacity", 0);
    }

    if(data.length < 100){

      const simulation = d3.forceSimulation(data)
        .force("x", d3.forceX(function(d) { return x(d[x_var]); }).strength(5))
        .force("y", d3.forceY(height / 2))
        .force("collide", d3.forceCollide(data[0].circleSize * 1.5))
        .stop();

      for (var i = 0; i < 120; ++i) simulation.tick();

      // Graph data points
      svg.append("g")
        .attr("stroke", "#505050")
        .attr("stroke-width", 1.5)
      .selectAll("circle")
        .data(data)
        .join("circle")
        .attr("id", d => d.areaID)
        .attr("class", "datapoints")
        .attr("cx", d => d.x)
        .attr("cy", d => d.y)
        .attr("r", d => d.circleSize)
        .attr("fill", d => d.colour)
        .on("mouseover", handleMouseOver)
        .on("mouseout", handleMouseOut);


    } else {
      // Set the y scale
      let y = d3.scaleLinear()
        .domain([-3, 3]).nice()
        .range([height - margin.bottom, margin.top]);

      let randomY = d3.randomBates(7);

     svg.append("g")
       .attr("stroke", "#505050")
       .attr("stroke-width", 0.25)
     .selectAll("circle")
       .data(data)
       .join("circle")
       .attr("id", d => d.areaID)
       .attr("class", "datapoints")
       .attr("cx", d => x(d[x_var]))
       .attr("cy", d => {return y((randomY() - 0.5) * 6)})
       .attr("r", d => d.circleSize)
       .attr("fill", d => d.colour)

         // Optional contours for LSOA scatterplots

         // let contours = d3.contourDensity()
         //   .x(d => x(d[x_var]))
         //   .y(d => {return y((randomY() - 0.5) * 6)})
         //   // .size([(width - margin.left - margin.right), (height - margin.top - margin.bottom)])
         //   .size([width, height])
         //   .bandwidth(20)
         //   .thresholds(30)
         //   (data)

         // svg.append("g")
         //    .attr("fill", "none")
         //    .attr("stroke", "#000")
         //    .attr("stroke-opacity", 0.40)
         //    .attr("stroke-linejoin", "round")
         //  .selectAll("path")
         //  .data(contours)
         //  .enter().append("path")
         //    .attr("stroke-width", (d, i) => i % 5 ? 0.25 : 1)
         //    .attr("d", d3.geoPath());

    }


  } // end drawBeeswarm

  // Calculate variables and redraw plot, recolour map
  function redraw(plotAreaId, chosen_supports, chosen_needs, data, height, width, margin, map, LAs, LSOAs){
    d3.select("#plot").remove();



    let boundaries, boundaries_source;

    let chosen_vars = chosen_supports.concat(chosen_needs);

    let chosen_objs = data.variables.filter(d => {
      return chosen_vars.includes(d.name);
    });

    if(chosen_objs.every(d => {
      return (d.lsoa === true);

      // Temporarily disable LSOA level
      // return false;
    })){
      data = data.LSOAs;
      boundaries = LSOAs;
      boundaries_source = "boundaries_LSOAs";
      data.forEach(d => {
        // d.areaID = d.LSOA11CD;
        // d.areaName = d.LSOA11NM;
        d.areaID = d.area_code;
        d.areaName = d.area_name;
        d.circleSize = 2;
        d.mapID = "LSOA11CD";
      });
      map.setLayoutProperty("LA_borders", 'visibility', 'none');
      map.setLayoutProperty("local_authorities", 'visibility', 'none');
  		map.setLayoutProperty("LSOA_borders", 'visibility', 'visible');
      map.setLayoutProperty("lower_super_output_areas", 'visibility', 'visible');
      console.log(data);
    } else {
      data = data.LAs;
      boundaries = LAs;
      boundaries_source = "boundaries_LAs";
      data.forEach(d => {
        // d.areaID = d.lad19cd;
        // d.areaName = d.lad19nm;
        d.areaID = d.area_code;
        d.areaName = d.area_name;
        d.circleSize = 6;
        d.mapID = "lad18cd";
      });
      map.setLayoutProperty("LA_borders", 'visibility', 'visible');
      map.setLayoutProperty("local_authorities", 'visibility', 'visible');
      map.setLayoutProperty("LSOA_borders", 'visibility', 'none');
      map.setLayoutProperty("lower_super_output_areas", 'visibility', 'none');
    }

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

      d3.select("i#axis_label").transition().duration(50).style("opacity", 1);
      d3.select("i#x_axis").transition().duration(50).style("opacity", 0);

      x_var = needs_var;
      if(supports_var !== null){
        y_var = supports_var;
        d3.select("i#y_axis").transition().duration(50).style("opacity", 1);

        // scatterplot
        cc.drawScatterplot(plotAreaId, x_var, y_var, data, height, width, margin, map, boundaries, boundaries_source);
      } else {
        d3.select("i#y_axis").transition().duration(50).style("opacity", 0);

        // beeswarm
        cc.drawBeeswarm(plotAreaId, x_var, data, height, width, margin, map, boundaries, boundaries_source, "need");
      }
    } else if(supports_var !== null){
      x_var = supports_var;

      d3.select("i#x_axis").transition().duration(50).style("opacity", 1);
      d3.select("i#y_axis").transition().duration(50).style("opacity", 0);
      d3.select("i#axis_label").transition().duration(50).style("opacity", 0);

      // beeswarm
      cc.drawBeeswarm(plotAreaId, x_var, data, height, width, margin, map, boundaries, boundaries_source, "support");
    } else {
      d3.select("i#x_axis").transition().duration(50).style("opacity", 0);
      d3.select("i#y_axis").transition().duration(50).style("opacity", 0);
      d3.select("i#axis_label").transition().duration(50).style("opacity", 0);

      map.setLayoutProperty("LA_borders", 'visibility', 'none');
      map.setLayoutProperty("local_authorities", 'visibility', 'none');
  		map.setLayoutProperty("LSOA_borders", 'visibility', 'none');
      map.setLayoutProperty("lower_super_output_areas", 'visibility', 'none');
    }
  } // end redraw

  // Colour ramp function adapted from https://observablehq.com/@mbostock/color-ramp
  function ramp(plot_area, color, n = 380) {
    const canvas = d3.select(plot_area).append("canvas")
      .attr("id", "canvas")
      .attr("width", 380)
      .attr("height", 10)
      .style("position", "absolute")
      .style("bottom", "5px")
      .style("left", "10px")
      // .style("margin-left", "10px")
      // .style("margin-top", "30px")
      .style("imageRendering", "crisp-edges");
    const context = canvas.node().getContext("2d");
    // canvas.style.margin = "0 -14px";
    // canvas.style.width = "400px";
    // canvas.style.height = "40px";
    // canvas.style.imageRendering = "crisp-edges";
    // canvas.style.imageRendering = "pixelated";
    for (let i = 0; i < n; ++i) {
      context.fillStyle = color(i / (n - 1));
      context.fillRect(i, 0, 1, 10);
    }
    return canvas;
  }

  return {
    drawScatterplot: drawScatterplot,
    drawBeeswarm: drawBeeswarm,
    redraw: redraw,
    getColourScale: getColourScale,
    getColourScale_support: getColourScale_support,
    getColourScale_need: getColourScale_need,
    getToggleAdder: getToggleAdder,
    z_score: z_score,
    sumOfZ: sumOfZ,
    ramp: ramp
  };
})(d3);
