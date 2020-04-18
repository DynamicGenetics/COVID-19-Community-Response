mapboxgl.accessToken = 'pk.eyJ1IjoibmluYWRpY2FyYSIsImEiOiJjazNsb3V3Ym0wNTdqM2JvaGRhdjFlN21vIn0.Q4kTCqSpKI00NAJzezecZg';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v10', // style: 'mapbox://styles/cmorenostokoe/ck8isca7j0zsk1iqx4k4khk4u'
    center: [-3.479368, 52.455248], //Mid-Wales ish
    zoom: 7
});

map.on('load', function () {

    // Add Source
    for (const layer of layers){
        map.addSource(layer.layerSpec.id,{
            'type': 'geojson',
            'data': layer.ref,
        });
    }

    // Add Layers
    for (const layer of layers){
        const visibility = layer.shownByDefault ? 'visible' : 'none';
        map.addLayer(layer.layerSpec);
        map.setLayoutProperty(layer.layerSpec.id, 'visibility', visibility);
    }
});


var menu = document.getElementById('menu');
var categoriesProcessed = []
var subheadings = {}

for (const layer of layers) {
    var id = layer.layerSpec.id;
    var name = layer.name;
    var checked = layer.shownByDefault;
    var category = layer.category;
    var colorsReversed = layer.colorsReversed;

    var container = document.createElement('div');
    var checkbox = document.createElement('input');
    var label = document.createElement('label');

    checkbox.type = 'checkbox';
    checkbox.value = id;
    checkbox.id = id;
    checkbox.checked = checked;
    checkbox.setAttribute('class', 'checkbox')

    label.setAttribute('for', id);
    
    if (colorsReversed == true){
        label.textContent = name.concat('*')
    } else {label.textContent = name}
    checkbox.addEventListener('change', checkboxChange);

    container.appendChild(checkbox);
    container.appendChild(label);

    //add item to legend for each category
    if (categoriesProcessed.includes(category)){
        subheadings[category].push(container)
        //console.log("apready processed: ", category)
    }else{
        subheadings[category]=[]
        subheadings[category].push(container)
        
        var subhead = document.createElement('div');
            subhead.innerHTML = `<strong> ${category} </strong>`
            subhead.className = 'menu-subhead';
            subhead.id = category

        var item = document.createElement('div');
        //get color stops
        for (const color_stop of layer.layerSpec.paint['fill-color'].stops) {
            var key = document.createElement('div');
            key.className = 'legend-key';
            key.style.backgroundColor = color_stop[1];
            if (colorsReversed == true){
                item.insertBefore(key, item.childNodes[0]);
            }else{
                item.appendChild(key);
            }
        }
        
        //append key and subheading
        subhead.append(item);
        subheadings[category].unshift(subhead);

        //make legend label text
        // var value = document.createElement('span');
        // value.innerHTML = category;
        // value.className = 'legend-label';
        // item.appendChild(value);

        //add category to completed list so key/label is not duplicated in legend
        categoriesProcessed.push(category);
    }
}

for (const cat of categoriesProcessed){
    for (const div of subheadings[cat]){
        menu.appendChild(div);
    }
}

function checkboxChange(evt) {
    var id = evt.target.value;
    var visibility = evt.target.checked ? 'visible' : 'none';
    map.setLayoutProperty(id, 'visibility', visibility);
}

map.on('mousemove', function(e) {
    var showVal = map.queryRenderedFeatures(e.point, {
      layers: ['groupCount_pop']
    });
    
    areaName = showVal[0].properties.lad18nm
    areaValue = showVal[0].properties.groupCount
  
    if (showVal.length > 0) {
      document.getElementById('pd').innerHTML = '<h3><strong>' + areaName + '</strong></h3><p><strong><em>' + areaValue + '</strong> groups </em></p>';
    } else {
      document.getElementById('pd').innerHTML = '<p>Hover over an area for values</p>';
    }
  });

/*
map.on('mousemove', function(e) {
    var showVal = map.queryRenderedFeatures(e.point, {
        layers: ['groupCount_pop']
    });

    if (showVal.length > 0) {
        document.getElementById('pd').innerHTML = '<h3><strong>' + showVal[0].properties.name + '</strong></h3><p><strong><em>' + showVal[0].properties.density + '</strong> people per square mile</em></p>';
    } else {
        document.getElementById('pd').innerHTML = '<p>Hover over a state!</p>';
    }
});
*/