// Set up sidebar
const sidebarWidth = 400;

// Opener / closer for sidebar
const addToggle = cc.getToggleAdder();
addToggle("div#sidebar", "div#content", sidebarWidth);

// Automatically close sidebar on smaller screens
const mq = window.matchMedia("(max-width: 813px)");
if (mq.matches) {
    const b = document.getElementById('opener');
    let evt = new MouseEvent("click");
    b.dispatchEvent(evt);
}

// Set up plotting area
const width=400;
const height=365;
// const margin = ({top: 30, right: 20, bottom: 40, left: 40});
const margin = ({top: 10, right: 22, bottom: 25, left: 48});

// Define a hidden div for tooltips
d3.select("#plot-container").append("div")
  .attr("class", "cc_tooltip")
  .style("opacity", 0);

// Add a color ramp legend
cc.ramp("#colour_scale", cc.getColourScale([0,1]));

// Load json data structure
const data_promise = d3.json("./frontend/map/data/data.json");

// Map boundaries data
const promiseLA = d3.json("./frontend/map/data/boundaries_LA.geojson");
const promiseLSOA = d3.json("./frontend/map/data/boundaries_LSOA.geojson");

// Load groups data
const promiseGroups = d3.json("./frontend/map/data/groups.geojson");

Promise.all([data_promise, promiseLA, promiseLSOA, promiseGroups]).then( data => {

  let LAs, LSOAs, groups;
  [data, LAs, LSOAs, groups] = data;

  const supports = data.variables.filter(d => d.class === "support");
  const needs = data.variables.filter(d => d.class === "challenge");

  // Set up selection input for supports
  d3.select("#multi-select_support input").property("value", supports[0].name);
  const support_menu = d3.select("#support_menu");
  supports.forEach(element => {
    support_menu.append("div").attr("class", "item").attr("data-value", element.name).html(element.label);
  });

  // Set up selection input for needs
  d3.select("#multi-select_needs input").property("value", needs[0].name);
  const needs_menu = d3.select("#needs_menu");
  needs.forEach(element => {
    needs_menu.append("div").attr("class", "item").attr("data-value", element.name).html(element.label);
  });

  // Select variables for page load
  let chosen_supports = [supports[0].name];
  let chosen_needs = [needs[0].name];

  // Set up map
  let map = new mapboxgl.Map({
    container: 'map',
    style: "mapbox://styles/oliverdavis/ck9q4pu7o5j4a1ipdqsxrusj2",
    // style: "mapbox://styles/mapbox/light-v9",
    center: [-3.766409, 52.33022],
    zoom: 7,
    bounds: [
      [-5.437896, 51.349480],
      [-2.487949, 53.460506]
    ]
  });

  // Navigation controls
  map.addControl(new mapboxgl.NavigationControl(), "bottom-left");

  // Remember the latest hovered map area
  let hoveredArea = null;

  map.on('load', function () {

    // Add map sources and layers
    map.addSource("boundaries_LAs", {
      "type": "geojson",
      "data": LAs,
      "generateId": true
    });
    map.addLayer({
      "id": "local_authorities",
      "type": "fill",
      "source": "boundaries_LAs",
      "layout": {
        "visibility": "none"
      },
      "paint": {
        'fill-color': ["get","colour"],
        'fill-opacity': ['interpolate', ["exponential", 2], ['zoom'], 7, 0.8, 13, 0.3]
      }
    }, "settlement-subdivision-label");
    // }, "road-simple");

    map.addLayer({
      "id": "LA_borders",
      "type": "line",
      "source": "boundaries_LAs",
      "layout": {
        "visibility": "none"
      },
      "paint": {
        "line-color": "#505050",
        "line-width": [
          "case",
          ["boolean", ["feature-state", "hover"], false],
          2,
          0.5
        ]
      }
    }, "settlement-subdivision-label");
    // }, "road-simple");


    map.addSource("boundaries_LSOAs", {
      "type": "geojson",
      "data": LSOAs,
      "generateId": true
    });
    map.addLayer({
      "id": "lower_super_output_areas",
      "type": "fill",
      "source": "boundaries_LSOAs",
      "layout": {
        "visibility": "none"
      },
      "paint": {
        'fill-color': ["get","colour"],
        'fill-opacity': ['interpolate', ["exponential", 6], ['zoom'], 7, 0.8, 13, 0.3]
      }
    }, "settlement-subdivision-label");
    // }, "road-simple");

    map.addLayer({
      "id": "LSOA_borders",
      "type": "line",
      "source": "boundaries_LSOAs",
      "layout": {
        "visibility": "none"
      },
      "paint": {
        "line-color": "#505050",
        "line-width": [
          "case",
          ["boolean", ["feature-state", "hover"], false],
          2,
          0
        ]
      }
    }, "settlement-subdivision-label");
    // }, "road-simple");


    map.addSource("groups_source", {type: "geojson", data: groups});
    map.addLayer({
      "id": "community_groups",
      "type": "circle",
      "source": "groups_source",
      "minzoom": 8,
      "layout": {
        "visibility": "visible"
      },
      "paint": {
        'circle-radius': ['interpolate', ["exponential", 1.75], ['zoom'], 9, 4, 14, 25],
        // "circle-color": "#747b7b"
        "circle-color": "#505050"
      }
    }, "settlement-subdivision-label");
    // }, "road-simple");

    // Hillshade layer (optional)
    // map.addSource('dem', {'type': 'raster-dem','url': 'mapbox://mapbox.terrain-rgb'});
    // map.addLayer({
    //   'id': 'hillshading',
    //   'source': 'dem',
    //   'type': 'hillshade'
    //   // insert below waterway-river-canal-shadow;
    //   // where hillshading sits in the Mapbox Outdoors style
    // }, 'waterway-shadow');

    // Draw plot of chosen variables, and colour map to match
    cc.redraw("#plot-area", chosen_supports, chosen_needs, data, height, width, margin, map, LAs, LSOAs);

    // Local authority mouse events
    map.on('mouseover', "local_authorities", function(e) {
    // Change the cursor style as a UI indicator.
      map.getCanvas().style.cursor = 'pointer';
    });

    map.on("mousemove", "local_authorities", function(e) {
      if (e.features.length > 0) {
        if (hoveredArea !== undefined) {
          map.setFeatureState(
            {source: "boundaries_LAs", id: hoveredArea},
            {hover: false}
          );
          if(e.features[0].id != hoveredArea){
            d3.selectAll("circle.datapoints")
              .transition().duration(50)
              .attr("r", "6").attr("stroke-width", 1.5);
          }
        }
        hoveredArea = e.features[0].id;
        map.setFeatureState(
          {source: "boundaries_LAs", id: hoveredArea},
          {hover: true}
        );
        let target = d3.select("circle#" + e.features[0].properties.lad18cd)
        target.transition().duration(50)
          .attr("r", "12").attr("stroke-width", 2);

        let x = target.attr("cx");
        let y = target.attr("cy");

        let tooltip_text = e.features[0].properties.lad18nm;
        let tooltip_width = (tooltip_text.length * 8) + 14;

        let tooltip = d3.select(".cc_tooltip");
        tooltip.html(tooltip_text)
          .style("width", tooltip_width + "px")
          .style("left", ((x - tooltip_width) + 15) + "px")
          .style("top", (y - 45) + "px");
        tooltip.transition().duration(50).style("opacity", 0.8);
      }
    });

    map.on('mouseleave', "local_authorities", function(e) {
      map.getCanvas().style.cursor = '';
      if(hoveredArea !== undefined) {
        map.setFeatureState(
          {source: "boundaries_LAs", id: hoveredArea},
          {hover: false}
        );
        d3.selectAll("circle.datapoints")
          .transition().duration(50)
          .attr("r", "6").attr("stroke-width", 1.5);
      }
      hoveredArea = null;

      let tooltip = d3.select(".cc_tooltip");
      tooltip.transition().duration(50).style("opacity", 0);

    });

    // LSOA events
    map.on('mouseover', "lower_super_output_areas", function(e) {
    // Change the cursor style as a UI indicator.
      map.getCanvas().style.cursor = 'pointer';
    });

    map.on("mousemove", "lower_super_output_areas", function(e) {
      if (e.features.length > 0) {
        if (hoveredArea !== undefined) {
          map.setFeatureState(
            {source: "boundaries_LSOAs", id: hoveredArea},
            {hover: false}
          );

          d3.select("#target_overlay").remove();
        }
        hoveredArea = e.features[0].id;
        map.setFeatureState(
          {source: "boundaries_LSOAs", id: hoveredArea},
          {hover: true}
        );

        let target = d3.select("circle#" + e.features[0].properties.LSOA11CD);
        let tx = target.attr("cx");
        let ty = target.attr("cy");
        let tfill = target.attr("fill");
        let overlay = d3.select("#plot-area").append("g").attr("id", "target_overlay");

        overlay.append("circle").attr("r", "6").attr("stroke", "#505050").attr("stroke-width", 1.5).attr("cx", tx).attr("cy", ty).attr("fill", tfill);

        let x = target.attr("cx");
        let y = target.attr("cy");

        let tooltip_text = e.features[0].properties.LSOA11NM;
        let tooltip_width = (tooltip_text.length * 8) + 14;

        let tooltip = d3.select(".cc_tooltip");
        tooltip.html(tooltip_text)
          .style("width", tooltip_width + "px")
          .style("left", ((x - tooltip_width) + 15) + "px")
          .style("top", (y - 39) + "px");
        tooltip.transition().duration(50).style("opacity", 0.8);

      }
    });

    map.on('mouseleave', "lower_super_output_areas", function(e) {
      map.getCanvas().style.cursor = '';
      if(hoveredArea !== undefined) {
        map.setFeatureState(
          {source: "boundaries_LSOAs", id: hoveredArea},
          {hover: false}
        );

        d3.select("#target_overlay").remove();
      }
      hoveredArea = null;

      let tooltip = d3.select(".cc_tooltip");
      tooltip.transition().duration(50).style("opacity", 0);

    });

    // Create a popup, but don't add it to the map yet.
    let popup = new mapboxgl.Popup({
      maxWidth: "none",
      className: "map_popup"
    });

    map.on('mouseover', "community_groups", function(e) {
    // Change the cursor style as a UI indicator
      map.getCanvas().style.cursor = 'pointer';
    });

    map.on('mouseleave', "community_groups", function(e) {
    // Change the cursor style as a UI indicator
      map.getCanvas().style.cursor = '';
    });

    map.on("click", "community_groups", function(e) {

      let coordinates = e.features[0].geometry.coordinates.slice();

      // Get group information
      let groupTitle = e.features[0].properties.Title;
      let groupSource = e.features[0].properties.Source;
      let groupURL = "<a href=\"" + e.features[0].properties.URL + "\" target=\"_blank\">" + e.features[0].properties.URL + "</a>"
      let groupLoc = e.features[0].properties.Location;

      // Combine group information into one description
      // let description = "<h4 style=\"margin-top:0px;\">Group Information</h4> <p><strong>Title:  </strong>" + groupTitle  + "<br><strong>Source: </strong>" + groupSource + "<br><strong>URL: </strong>" + groupURL + "<br><strong>Location:  </strong>" + groupLoc + "</p>"
      let description = `<h4>${groupTitle}</h4>
                        <p><strong>Location:</strong> ${groupLoc}</p>
                        <p><strong>URL:</strong> ${groupURL}</p>
                        <p><strong>Source:</strong> ${groupSource}</p>`

      // Ensure that if the map is zoomed out such that multiple
      // copies of the feature are visible, the popup appears
      // over the copy being pointed to.
      while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
      }

      // Populate the popup and set its coordinates
      // based on the feature found.
      popup.setLngLat(coordinates)
        .setHTML(description)
        .addTo(map);

    });

  });

  // Set up variable selection drop-downs
  $('#multi-select_support')
    .dropdown({
      // useLabels: false,
      onChange: handleSelectionChange
    });
  $('#multi-select_support').dropdown('set value', supports[0].name);

  $('#multi-select_needs')
    .dropdown({
      // useLabels: false,
      onChange: handleSelectionChange
    });

  // Redraw when the selected variables change
  function handleSelectionChange(value, text, $selectedItem) {

    chosen_supports = d3.select("#multi-select_support input").property("value").split(',');
    if(chosen_supports[0] === ""){
      chosen_supports = [];
    }
    chosen_needs = d3.select("#multi-select_needs input").property("value").split(',');
    if(chosen_needs[0] === ""){
      chosen_needs = [];
    }
    cc.redraw("#plot-area", chosen_supports, chosen_needs, data, height, width, margin, map, LAs, LSOAs);
  }


});
