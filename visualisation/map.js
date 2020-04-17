mapboxgl.accessToken = 'pk.eyJ1IjoibmluYWRpY2FyYSIsImEiOiJjazNsb3V3Ym0wNTdqM2JvaGRhdjFlN21vIn0.Q4kTCqSpKI00NAJzezecZg';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', //mapbox://styles/cmorenostokoe/ck8isca7j0zsk1iqx4k4khk4u
    center: [-3.479368, 52.455248], //Mid-Wales ish
    zoom: 7
});

map.on('load', function () {

    //Add sources
    // map.addSource('local-authority-boundaries', {
    //     'type': 'geojson',
    //     'data': '../data/boundaries_LAs.geoJSON'
    // });

    layers.forEach(function(e){
        map.addSource(e.layerSpec.id, {
            'type': 'geojson',
            'data': e.layerSpec.source
        });
    });

    //Add layers
    for (const layer of layers) {
        const visibility = layer.shownByDefault ? 'visible' : 'none';
        map.addLayer(layer.layerSpec);
        map.setLayoutProperty(layer.layerSpec.id, 'visibility', visibility);
    }
});


var menu = document.getElementById('menu');

for (const layer of layers) {
    var id = layer.layerSpec.id;
    var name = layer.name;
    var checked = layer.shownByDefault;

    var container = document.createElement('div');
    var checkbox = document.createElement('input');
    var label = document.createElement('label');

    checkbox.type = 'checkbox';
    checkbox.value = id;
    checkbox.id = id;
    checkbox.checked = checked;
    checkbox.setAttribute('class', 'checkbox')

    label.setAttribute('for', id);
    label.textContent = name;

    checkbox.addEventListener('change', checkboxChange);

    container.appendChild(checkbox);
    container.appendChild(label);

    menu.appendChild(container);
}

function checkboxChange(evt) {
    var id = evt.target.value;
    var visibility = evt.target.checked ? 'visible' : 'none';
    map.setLayoutProperty(id, 'visibility', visibility);


}
