mapboxgl.accessToken = 'pk.eyJ1IjoibmluYWRpY2FyYSIsImEiOiJjazNsb3V3Ym0wNTdqM2JvaGRhdjFlN21vIn0.Q4kTCqSpKI00NAJzezecZg';
const map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v10', // style: 'mapbox://styles/cmorenostokoe/ck8isca7j0zsk1iqx4k4khk4u'
    center: [-3.479368, 52.455248], //Mid-Wales ish
    zoom: 7
});

let visibleLayers = []
let nickNames = {}

map.on('load', function () {

    // Add Source
    for (const layer of layers) {
        map.addSource(layer.layerSpec.id, {
            'type': 'geojson',
            'data': layer.ref,
        });
    }

    // Add Layers
    for (const layer of layers) {
        const visibility = layer.shownByDefault ? 'visible' : 'none';
        map.addLayer(layer.layerSpec);
        map.setLayoutProperty(layer.layerSpec.id, 'visibility', visibility);
        if (visibility === 'visible') {
            visibleLayers.push(layer.layerSpec.id)
        }
        nickNames[layer.layerSpec.id] = layer.name
    }
});


// Dynamically generate sidebar menu & integrated legend

let menu = document.getElementById('menu');
let categoriesProcessed = []
let subheadings = {}
let orders = {}

for (const layer of layers) {
    console.log(layer.name)
    const id = layer.layerSpec.id;
    const name = layer.name;
    const checked = layer.shownByDefault;
    const category = layer.category;
    const displayOrder = layer.displayOrder;
    const colorsReversed = layer.colorsReversed;
    const layerType = layer.layerSpec.type;

    let container = document.createElement('div');
    let checkbox = document.createElement('input');
    let label = document.createElement('label');

    checkbox.type = 'checkbox';
    checkbox.value = id;
    checkbox.id = id;
    checkbox.checked = checked;
    checkbox.setAttribute('class', 'checkbox dense')

    label.setAttribute('for', id);
    label.setAttribute('class', 'dense');

    if (colorsReversed === true) {
        label.textContent = name.concat('*')
    } else {
        label.textContent = name
    }
    checkbox.addEventListener('change', checkboxChange);

    container.appendChild(checkbox);
    container.appendChild(label);

    //add item to legend for each category
    if (categoriesProcessed.includes(category)) {
        subheadings[category].push(container)

    } else {

        subheadings[category] = []
        subheadings[category].push(container)

        //Build headings & legends for categories
        if (layerType !== 'circle') {

            let subhead = document.createElement('div');
            subhead.innerHTML = `<strong> ${category} </strong>`
            subhead.className = 'menu-subhead';
            subhead.setAttribute('class', 'dense');
            subhead.id = category

            let item = document.createElement('div');

            //get color stops
            for (const color_stop of layer.layerSpec.paint['fill-color'].stops) {
                let key = document.createElement('div');
                key.className = 'legend-key';
                key.style.backgroundColor = color_stop[1];
                if (colorsReversed === true) {
                    item.insertBefore(key, item.childNodes[0]);
                } else {
                    item.appendChild(key);
                }
            }

            //append key and subheading
            subhead.append(item);
            subheadings[category].unshift(subhead);
        }
        categoriesProcessed.push(category);
        orders[category] = displayOrder
    }
}

categoriesOrdered = []
//Order categories and append to menu
for (const o of categoriesProcessed) {
    categoriesOrdered.push([orders[o], o])
}
categoriesOrdered.sort()

for (const cat of categoriesOrdered) {
    for (const div of subheadings[cat[1]]) {
        menu.appendChild(div);
    }

}

function checkboxChange(evt) {
    let id = evt.target.value;
    let visibility = evt.target.checked ? 'visible' : 'none';

    map.setLayoutProperty(id, 'visibility', visibility);

    if (visibleLayers.includes(id)) {
        const index = visibleLayers.indexOf(id);
        if (index > -1) {
            visibleLayers.splice(id, 1);
        }
    } else {
        visibleLayers.push(id);
    }
}


// Sidebar opener and closer
const sdbr = d3.select("div.sidebar");
const bdy = d3.select("body");
const open_close = bdy.append("svg").attr("id", "open_close");
open_close.append("circle").attr("id", "opener").attr("cx", 20).attr("cy", 20).attr("r", 20).attr("fill", "#fff").attr("opacity", 0.5);
let sidebar_open = true;
const cross_lines = open_close.append("g").attr("class", "cross_lines");
cross_lines.append("path").attr("d", "M 20 10 V 30").attr("stroke", "#4c4c4c").attr("stroke-width", 4).attr("stroke-linecap", "round");
cross_lines.append("path").attr("d", "M 10 20 H 30").attr("stroke", "#4c4c4c").attr("stroke-width", 4).attr("stroke-linecap", "round");
open_close.style("transform", "rotate(-45deg)");

d3.select("#opener").on("click", e => {
    if (sidebar_open) {
        sdbr.transition().duration(750).style("right", "-23rem");
        open_close.transition().duration(750).style("transform", "rotate(90deg)");
        sidebar_open = false;
    } else {
        sdbr.transition().duration(750).style("right", "0rem");
        open_close.transition().duration(750).style("transform", "rotate(-45deg)");
        sidebar_open = true;
    }
});

// Mouse - over data pop up
map.on('mousemove', function (e) {

    let defaultTag = "<p>Hover over an area for values</p>";
    document.getElementById('pd').innerHTML = '';

    let features = map.queryRenderedFeatures(e.point, {
        layers: visibleLayers
    });

    if (features.length > 0) {

        let areaName, name, nickName, areaValue;
        // Reducer function to concatenate visible layers info
        const reducer = (tag, paragraph) => tag + paragraph;

        if (features[0].properties.hasOwnProperty('lad18nm')) {
            areaName = features[0].properties.lad18nm
        } else if (features[0].properties.hasOwnProperty('areaID')) {
            areaName = features[0].properties.areaID
        } else {
            areaName = '';
        }

        let htmlText = '<div class="pd_p"><h3><strong>' + areaName + '</strong></h3>';

        // for (let feature in features) {
        let htmlParagraphs = features.reverse().map(function (feature) {
            name = feature.layer.id
            nickName = nickNames[name]
            areaValue = feature.properties[name]
            if (areaValue === undefined)  // this may happen when we have only Community Support Group Visible
                return "";
            if (areaValue < 0.001) {
                areaValue = areaValue.toFixed(4)
            } else if (areaValue < 1) {
                areaValue = areaValue.toFixed(2)
            } else if (areaValue.countDecimals() > 4) {
                areaValue = areaValue.toFixed(1)
            }
            return "<p>" + nickName + ": <strong>" + areaValue + "</strong></p>";
        });
        htmlText += htmlParagraphs.reduce(reducer);
        htmlText += "</div>";
        // }
        document.getElementById('pd').innerHTML = htmlText
        //document.getElementById('pd').innerHTML = '<h3><strong>' + areaName + '</strong></h3><p><strong><em>' + (areaValue*divisor).toFixed(2) + '</strong> groups per '  + divisor + ' people </em></p>';
    } else {
        document.getElementById('pd').innerHTML = defaultTag;
    }
});

Number.prototype.countDecimals = function () {
    if (Math.floor(this.valueOf()) === this.valueOf()) return 0;
    return this.toString().split(".")[1].length || 0;
}
