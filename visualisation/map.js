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


// Dynamically generate sidebar menu & integrated legend

var menu = document.getElementById('menu');
var categoriesProcessed = []
var subheadings = {}
var orders = {}

for (const layer of layers) {
    console.log(layer.name)
    var id = layer.layerSpec.id;
    var name = layer.name;
    var checked = layer.shownByDefault;
    var category = layer.category;
    var displayOrder = layer.displayOrder;
    var colorsReversed = layer.colorsReversed;
    var layerType = layer.layerSpec.type;

    var container = document.createElement('div');
    var checkbox = document.createElement('input');
    var label = document.createElement('label');

    checkbox.type = 'checkbox';
    checkbox.value = id;
    checkbox.id = id;
    checkbox.checked = checked;
    checkbox.setAttribute('class', 'checkbox dense')

    label.setAttribute('for', id);
    label.setAttribute('class', 'dense');
    
    if (colorsReversed == true){
        label.textContent = name.concat('*')
    } else {label.textContent = name}
    checkbox.addEventListener('change', checkboxChange);

    container.appendChild(checkbox);
    container.appendChild(label);

    //add item to legend for each category        
    if (categoriesProcessed.includes(category)){
        subheadings[category].push(container)
        
    }else{
        
        subheadings[category]=[]
        subheadings[category].push(container)

        //Build headings & legends for categories
        if (layerType != 'circle'){

            var subhead = document.createElement('div');
                subhead.innerHTML = `<strong> ${category} </strong>`
                subhead.className = 'menu-subhead';
                subhead.setAttribute('class', 'dense');
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
        }
        categoriesProcessed.push(category);
        orders[category]=displayOrder
    }
}

categoriesOrdered=[]
//Order categories and append to menu
for (const o of categoriesProcessed){
    categoriesOrdered.push([orders[o],o])
}
categoriesOrdered.sort()

for (const cat of categoriesOrdered){
    for (const div of subheadings[cat[1]]){
        menu.appendChild(div);
    }

}

function checkboxChange(evt) {
    var id = evt.target.value;
    var visibility = evt.target.checked ? 'visible' : 'none';

    map.setLayoutProperty(id, 'visibility', visibility);

    if (visibleLayers.includes(id)){

        const index = visibleLayers.indexOf(id);
        if (index > -1) {
            visibleLayers.splice(id, 1);
        }

    }else{

        visibleLayers.push(id)
    }
}


// Mouse - over data pop up
map.on('mousemove', function(e) {

    var showVal = map.queryRenderedFeatures(e.point, {
      layers: visibleLayers
    });
    
    if (typeof(showVal[0].properties.lad18nm)=="string"){
        areaName = showVal[0].properties.lad18nm
    } else if (typeof(showVal[0].properties.areaID)=="string"){
        areaName = showVal[0].properties.areaID
    }
  
    if (showVal.length > 0) {
        htmlText = '<p class="pd_p"><h3><strong>' + areaName + '</strong></h3>';

        for (i in showVal){
            name = showVal[i].layer.id
            nickName = nickNames[name]
            areaValue = showVal[i].properties[name]
            if (areaValue < 0.001) {
                areaValue=areaValue.toFixed(4)
            } else if  (areaValue < 1){
                areaValue=areaValue.toFixed(2)
            } else if (areaValue.countDecimals()>4) {
                areaValue=areaValue.toFixed(1)
            }
            
            htmlText = htmlText + nickName + ': <strong><em>' + areaValue + '</em></strong></p>';
        }
        document.getElementById('pd').innerHTML = htmlText
      //document.getElementById('pd').innerHTML = '<h3><strong>' + areaName + '</strong></h3><p><strong><em>' + (areaValue*divisor).toFixed(2) + '</strong> groups per '  + divisor + ' people </em></p>';
    } else {
      document.getElementById('pd').innerHTML = '<p>Hover over an area for values</p>';
    }
  });

Number.prototype.countDecimals = function () {
    if(Math.floor(this.valueOf()) === this.valueOf()) return 0;
    return this.toString().split(".")[1].length || 0; 
}