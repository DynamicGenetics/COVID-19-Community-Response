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
      .range(["#3781ff","#f0f0f0","#c32b38"])
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

  // Add the scatter plot
  function drawScatterplot(targetArea, x, y){

  }

  // Add the beeswarm plot
  function drawBeeswarm(targetArea, x, y){

  }

  return {
    drawScatterplot: drawScatterplot,
    drawBeeswarm: drawBeeswarm,
    getColourScale: getColourScale,
    getToggleAdder: getToggleAdder
  };
})(d3);
