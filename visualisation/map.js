mapboxgl.accessToken = 'pk.eyJ1IjoibmluYWRpY2FyYSIsImEiOiJjazNsb3V3Ym0wNTdqM2JvaGRhdjFlN21vIn0.Q4kTCqSpKI00NAJzezecZg';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/light-v10', // style: 'mapbox://styles/cmorenostokoe/ck8isca7j0zsk1iqx4k4khk4u'
    center: [-3.479368, 52.455248], //Mid-Wales ish
    zoom: 7
});

var extra_layers = [
    {
        name: 'Tweets by LA Population',
        shownByDefault: false,
        layerSpec: {
            id: 'tweet',
            type: 'fill',
            source: 'tweet',
            paint: {
                'fill-color': {
                    property: 'tweets_per_pop',
                    stops: [[0.1, '#F7FBFF'],
                            [0.2, '#DEEBF7'],
                            [0.3, '#C6DBEF'],
                            [0.4, '#9ECAE1'],
                            [0.5, '#6BAED6'],
                            [0.6, '#4292C6'],
                            [0.7, '#2171B5'],
                            [0.8, '#984887'],
                            [0.9, '#08519C'],
                            [1, '#08306B']]
                },
                'fill-opacity': 0.46666666666666666
            },
            filter: ['==', '$type', 'Polygon']
        }
    },
    ];

map.on('load', function () {

    // Add Source
    for (const layer of layers){
        map.addSource(layer.layerSpec.id,{
            'type': 'geojson',
            'data': layer.ref,
        });
    }

    map.addSource('tweet', {
        'type': 'geojson',
        'data': '../data/twitter_count.geojson'
        });

    // Add Layers
    for (const layer of layers){
        const visibility = layer.shownByDefault ? 'visible' : 'none';
        map.addLayer(layer.layerSpec);
        map.setLayoutProperty(layer.layerSpec.id, 'visibility', visibility);
    }

    for (const layer of extra_layers){
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

for (const layer of extra_layers) {
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

for (i = 0; i < layers.length; i++) {
    var layer = layer[i];
    var color = 'red';
    var item = document.createElement('div');
    var key = document.createElement('span');
    key.className = 'legend-key';
    key.style.backgroundColor = color;
  
    var value = document.createElement('span');
    value.innerHTML = layer;
    item.appendChild(key);
    item.appendChild(value);
    legend.appendChild(item);
  }