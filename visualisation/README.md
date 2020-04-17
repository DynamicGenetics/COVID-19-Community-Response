#  Mapbox Web App

To run the webapp locally: 
- Start a local Python web server in the root folder of the repository using cmd `python -m http.server`  
- Open up `index.html`  
- Go to the local host address in your web browser, and navigate to `visualisation`.

Resources used:
- Geojson files from geoJSON folder.   
- Generic mapbox documentation on plotting points and polygons from geojson, including 'data-driven' styling for the properties of the geojson.  
- The code from [this page on toggling layers of the map](https://docs.mapbox.com/mapbox-gl-js/example/toggle-layers/)  
- The file `demographics_withstops.xlsx` contains my workings for generating the colour stops that are used in the geojson layers. (Sorry, it's in Excel...). The colours were generated using [this automatic palette generator](https://gka.github.io/palettes).  
