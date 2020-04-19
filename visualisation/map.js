mapboxgl.accessToken = 'pk.eyJ1IjoibmluYWRpY2FyYSIsImEiOiJjazNsb3V3Ym0wNTdqM2JvaGRhdjFlN21vIn0.Q4kTCqSpKI00NAJzezecZg';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v10', // style: 'mapbox://styles/cmorenostokoe/ck8isca7j0zsk1iqx4k4khk4u'
    center: [-3.479368, 52.455248], //Mid-Wales ish
    zoom: 7
});

var visibleLayers=[]
var nickNames={}

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
        if (visibility=='visible'){visibleLayers.push(layer.layerSpec.id)}
        nickNames[layer.layerSpec.id]=layer.name
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
    if (visibleLayers.includes(id)){
        visibleLayers.pop(id)
    }else{visibleLayers.push(id)}
}

map.on('mousemove', function(e) {

    //console.log("visible:",visibleLayers)

    var showVal = map.queryRenderedFeatures(e.point, {
      layers: visibleLayers
    });
    
    if (typeof(showVal[0].properties.lad18nm)=="string"){
        areaName = showVal[0].properties.lad18nm
    } else if (typeof(showVal[0].properties.areaID)=="string"){
        areaName = showVal[0].properties.areaID
        console.log(showVal[0].properties)
    }
  
    if (showVal.length > 0) {
        htmlText = []
        htmlText.push('<p class="pd_p"><h3><strong>' + areaName + '</strong></h3>')

        for (i in showVal){
            name = showVal[i].layer.id
            nickName = nickNames[name]
            areaValue = showVal[i].properties[name]
            htmlText.push(nickName + ': <strong><em>' + areaValue.toFixed(4) + '</em></strong></p>');
        }
        document.getElementById('pd').innerHTML = htmlText
      //document.getElementById('pd').innerHTML = '<h3><strong>' + areaName + '</strong></h3><p><strong><em>' + (areaValue*divisor).toFixed(2) + '</strong> groups per '  + divisor + ' people </em></p>';
    } else {
      document.getElementById('pd').innerHTML = '<p>Hover over an area for values</p>';
    }
  });