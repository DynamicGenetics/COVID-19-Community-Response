mapboxgl.accessToken = 'pk.eyJ1IjoibmluYWRpY2FyYSIsImEiOiJjazNsb3V3Ym0wNTdqM2JvaGRhdjFlN21vIn0.Q4kTCqSpKI00NAJzezecZg';
var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11', //mapbox://styles/cmorenostokoe/ck8isca7j0zsk1iqx4k4khk4u
    center: [-3.479368, 52.455248], //Mid-Wales ish
    zoom: 7
});

var layers = [
    {
        name: 'Local authority boundaries',
        shownByDefault: true,
        layerSpec: {
            id: 'local-authority-boundaries',
            type: 'line',
            source: 'local-authority-boundaries',
            layout: {},
            paint: {
                'line-color': '#088',
                'line-opacity': 1.0
            }
        }
    },
    {
        name: 'Known groups',
        shownByDefault: true,
        layerSpec: {
            id: 'known-groups',
            type: 'circle',
            source: 'known-groups',
            paint: {
                'circle-radius': {
                    base: 1.75,
                    stops: [[12, 2], [22, 180]]
                },
                'circle-color': '#223b53'
            }
        }
    },
    {
        name: 'Index of multiple deprivation',
        shownByDefault: false,
        layerSpec: {
            id: 'deprivation',
            type: 'fill',
            source: 'demographics',
            paint: {
                'fill-color': {
                    property: 'deprivation_30',
                    stops: [[5, '#ffcaff'],
                            [10.9, '#f0b7ed'],
                            [16.8, '#e1a4db'],
                            [22.7, '#d391ca'],
                            [28.6, '#c47fb9'],
                            [34.5, '#b56da8'],
                            [40.4, '#a75b98'],
                            [46.3, '#984887'],
                            [52.2, '#8a3678'],
                            [64, '#7b2268']]
                },
                'fill-opacity': 0.5
            },
            filter: ['==', '$type', 'Polygon']
        }
    },
    {
        name: 'Population density',
        shownByDefault: false,
        layerSpec: {
            id: 'pop_density',
            type: 'fill',
            source: 'demographics',
            paint: {
                'fill-color': {
                    property: 'pop_density',
                    stops: [[25.6, '#ffff87'],
                            [281.56, '#fff77f'],
                            [537.52, '#ffef77'],
                            [793.48, '#ffe770'],
                            [1049.44, '#ffdf68'],
                            [1305.4, '#ffd760'],
                            [1561.36, '#ffcf58'],
                            [1817.32, '#ffc750'],
                            [2073.28, '#ffbe48'],
                            [2585.2, '#ffb63f']]
                },
                'fill-opacity': 0.5
            },
            filter: ['==', '$type', 'Polygon']
        }
    },
    {
        name: 'Elderly population',
        shownByDefault: false,
        layerSpec: {
            id: 'pop_elderly',
            type: 'fill',
            source: 'demographics',
            paint: {
                'fill-color': {
                    property: 'pop_elderly',
                    stops: [[14.09451802, '#91e5ff'],
                            [15.429026416, '#84d3f3'],
                            [16.763534812, '#77c2e7'],
                            [18.098043208, '#6ab1da'],
                            [19.432551604, '#5da0ce'],
                            [20.76706, '#4f90c3'],
                            [22.101568396, '#417fb7'],
                            [23.436076792, '#3270ab'],
                            [24.770585188, '#1f609f'],
                            [27.43960198, '#005194']]
                },
                'fill-opacity': 0.5
            },
            filter: ['==', '$type', 'Polygon']
        }
    },
    {
        name: 'Language',
        shownByDefault: false,
        layerSpec: {
            id: 'language',
            type: 'fill',
            source: 'demographics',
            paint: {
                'fill-color': {
                    property: 'language',
                    stops: [[4.8, '#e689ff'],
                            [10.83, '#d87cf6'],
                            [16.86, '#ca70ed'],
                            [22.89, '#bd63e3'],
                            [28.92, '#af56da'],
                            [34.95, '#a249d1'],
                            [40.98, '#943cc8'],
                            [47.01, '#862fbf'],
                            [53.04, '#7820b6'],
                            [65.1, '#6a0dad']]
                },
                'fill-opacity': 0.5
            },
            filter: ['==', '$type', 'Polygon']
        }
    },
    {
        name: 'Number of groups',
        shownByDefault: false,
        layerSpec: {
            id: 'groupsCount',
            type: 'fill',
            source: 'known-groups_count',
            paint: {
                'fill-color': {
                    property: 'groupCount',
                    stops: [[4.8, '#e689ff'],
                            [10.83, '#d87cf6'],
                            [16.86, '#ca70ed'],
                            [22.89, '#bd63e3'],
                            [28.92, '#af56da'],
                            [34.95, '#a249d1'],
                            [40.98, '#943cc8'],
                            [47.01, '#862fbf'],
                            [53.04, '#7820b6'],
                            [65.1, '#6a0dad']]
                },
                'fill-opacity': 0.5
            },
            filter: ['==', '$type', 'Polygon']
        }
    },
    {
        name: 'Number of groups by population',
        shownByDefault: false,
        layerSpec: {
            id: 'groupsCount_pop',
            type: 'fill',
            source: 'known-groups_count',
            paint: {
                'fill-color': {
                    property: 'groupCount_pop',
                    stops: [[4.8, '#e689ff'],
                            [10.83, '#d87cf6'],
                            [16.86, '#ca70ed'],
                            [22.89, '#bd63e3'],
                            [28.92, '#af56da'],
                            [34.95, '#a249d1'],
                            [40.98, '#943cc8'],
                            [47.01, '#862fbf'],
                            [53.04, '#7820b6'],
                            [65.1, '#6a0dad']]
                },
                'fill-opacity': 0.5
            },
            filter: ['==', '$type', 'Polygon']
        }
    },
    {
        name: 'Number of groups by elderly population',
        shownByDefault: false,
        layerSpec: {
            id: 'groupsCount_elderly',
            type: 'fill',
            source: 'known-groups_count',
            paint: {
                'fill-color': {
                    property: 'groupCount_elderly',
                    stops: [[4.8, '#e689ff'],
                            [10.83, '#d87cf6'],
                            [16.86, '#ca70ed'],
                            [22.89, '#bd63e3'],
                            [28.92, '#af56da'],
                            [34.95, '#a249d1'],
                            [40.98, '#943cc8'],
                            [47.01, '#862fbf'],
                            [53.04, '#7820b6'],
                            [65.1, '#6a0dad']]
                },
                'fill-opacity': 0.5
            },
            filter: ['==', '$type', 'Polygon']
        }
    }
];

map.on('load', function () {

    //Add sources
    map.addSource('local-authority-boundaries', {
        'type': 'geojson',
        'data': '../data/boundaries_LAs.geoJSON'
    });

    map.addSource('demographics', {
        'type': 'geojson',
        'data': '../data/demographics_floats.geojson'
    });

    map.addSource('known-groups_count', {
        'type': 'geojson',
        'data': '../data/groupCount.geojson'
    });

    map.addSource('known-groups', {
        'type': 'geojson',
        'data': '../data/groups.geojson'
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