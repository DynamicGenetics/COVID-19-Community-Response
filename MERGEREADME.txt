metadata + processing file


Additions
- raw folder to geoboundaries to store raw unfiltered geoboundary data

Changes

Changes to python data functions (previously borg)
- data/static/geography to data/geography for clarity
- borg file split  into seperate updateData and generateLayer functions (borg.py --> masterScripts updateData & createMapLayers)
- layer filename change (borgLayers --> layers)
- reformatted data pipeline to comply with Nina's folder restructure
- better commented files

Changes to layers.js
- renamed (borgLayers.js --> layers.js)

Changes to maps.js
- filestructure changes to reflect restructuring

Changes to index.html
- fixed jquery theme not applying (typo in href)

Issues introduced
- disabled group count per LSOA map layer (this section of pipeline broken)