#  Mapbox Web - log

### 31st March 2020 - `@ninadicara`  
I've had a go at putting the geojson files onto mapbox.   

To run: 
- Start a local Python web server using cmd `python -m http.server`  
- Open up `index.html`  
- In the top right-hand corner you should see a list of boxes with the names of layers. They default as 'visible', but if you click the names it should hide them.   

Resources used:
- Geojson files from geoJSON folder.   
- Generic mapbox documentation on plotting points and polygons from geojson, including 'data-driven' styling for the properties of the geojson.  
- The code from [this page on toggling layers of the map](https://docs.mapbox.com/mapbox-gl-js/example/toggle-layers/)  
- The file `demographics_withstops.xlsx` contains my workings for generating the colour stops that are used in the geojson layers. (Sorry, it's in Excel...). The colours were generated using [this automatic palette generator](https://gka.github.io/palettes).  
