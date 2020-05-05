import json
from statistics import stdev

"""
Intended script purpose:
1. Iterate over each data source in data sources,
2. Build a dictionary of metadata for each datafield in each data source,
3. Output objective JS formatted layers (to layers.js)

Formatting is intended to be usable directly by the maps.js 
(i.e., objective JS dictionary of dataField metadata)
"""

# Specify data fields to ignore (e.g., ONS shape descriptor values)
geoLabelsToIgnore = ["objectid", "bng_e", "bng_n"]

# Generate a map layer for each data layer in each data source
def generate_layer_JS(dataSources, filename_output):

    # Initialise output list, exceptions and layers lists for methods to populate
    output = []
    exceptions = []
    layers = {}

    def main():

        # Intitialise list and count of finished layers
        finishedLayers = []
        o = 0

        # Build dictionary entries for the metadata for each datafield in data sources
        for src in dataSources:

            # Skip if data source is disabled ('enabled' == False)
            if src["enabled"]:

                # Process for point geometry (doesn't require data stops):
                if src["geometry"] == "Points":
                    discoverPointDataField(src)

                # Process for other geometries (e.g., polygon requires data stops):
                elif src["geometry"] == "Polygons":
                    discoverPolygonDataField(src)

        # Use dictionaries to produce layers formatted in objective JS
        for key_category in layers:

            # Get category of layer from dataField metadata dictionary entry
            layerCategory = layers[key_category]

            for key_layer in layerCategory:

                # Get properties of layers under category
                layer = layerCategory[key_layer]

                # Now process point data
                if layer["geometry"] == "Polygons":
                    dataField = producePolygonLayer(layerCategory, layer)
                    finishedLayers.append(dataField)

                # Now process point data
                elif layer["geometry"] == "Points":
                    dataField = producePointsLayer(layerCategory, layer)
                    finishedLayers.append(dataField)

            # Increment layer count
            o += 1

        with open(filename_output, "w") as outs:
            jsonDumps = json.dumps(output, indent=4, sort_keys=True)
            outs.write("var layers={}".format(jsonDumps))

        return "Message (generateLayers): Layers produced: {} ({}). Exceptions: {}".format(
            len(output), finishedLayers, len(set(exceptions))
        )

    def discoverPointDataField(src):

        # Detect data fields in data sources
        for dataField in src["layers"].keys():
            layer = src["layers"][dataField]

            # Skip disabled data fields (in dataSources)
            if not layer["disabled"]:

                # Get category of data field from dataSources metadata
                category = layer["categoryInfo"]["name"]

                # Initialise dictionary entry if doesn't exist
                if category not in layers.keys():
                    layers[category] = {}

                # Make dictionary entry for data field
                layers[category][dataField] = {
                    "dataField": dataField,
                    "origin": src["name"],
                    "path": src["path"],
                    "nickName": layer["nickName"],
                    "reverseColors": layer["reverseColors"],
                    "geometry": src["geometry"],
                    "values": None,
                    "ID_name": src["ID_name"],
                    "categoryInfo": layer["categoryInfo"],
                    "enabledByDefault": layer["enabledByDefault"],
                }

    def discoverPolygonDataField(src):

        # Get filepath to geojson file for all data fields in data source
        filename = "dashboard/data/{}.geojson".format(src["name"])

        with open(filename, "r") as geojson_file:

            # For row in geoJSON, count values and assign color values
            geojson = json.load(geojson_file)
            for feature in geojson["features"]:
                properties = feature["properties"]

                # If dataField in dataSource found AND not disabled then process further
                for dataField in properties.keys():
                    if dataField in src["layers"].keys():
                        layer = src["layers"][dataField]

                        if not layer["disabled"]:

                            dataValue = properties[dataField]

                            category = layer["categoryInfo"]["name"]

                            if category not in layers.keys():
                                layers[category] = {}

                            if dataField not in layers[category].keys():
                                layers[category][dataField] = {
                                    "dataField": dataField,
                                    "origin": src["name"],
                                    "path": src["path"],
                                    "nickName": layer["nickName"],
                                    "reverseColors": layer["reverseColors"],
                                    "geometry": src["geometry"],
                                    "dataValues": [dataValue],
                                    "ID_name": src["ID_name"],
                                    "enabledByDefault": layer["enabledByDefault"],
                                    "categoryInfo": layer["categoryInfo"],
                                }
                            else:
                                layers[category][dataField]["dataValues"].append(
                                    dataValue
                                )

                            # print("Added layer: ", layer)

                        else:
                            exceptions.append("{}(disabled)".format(dataField))

                    else:
                        exceptions.append(dataField)
                        # print("Warning (generateLayer): datafield found in dataSource not specified in dataSources")

    def producePolygonLayer(layerCategory, layer):

        # Get metadata for each field from metadata dictionary entry
        dataField = layer["dataField"]
        origin = layer["origin"]
        category = layer["categoryInfo"]["name"]
        hexList = layer["categoryInfo"]["colors"]
        displayOrder = layer["categoryInfo"]["displayOrder"]
        nickName = layer["nickName"]
        reverseColors = layer["reverseColors"]
        geometry = layer["geometry"]
        ID_name = layer["ID_name"]
        enabledByDefault = layer["enabledByDefault"]

        dataValues = layer["dataValues"]
        stops = []

        # Get range of each property dataField in geoJSON (if numeric)
        if isinstance(dataValues[0], int) or isinstance(dataValues[0], float):

            # Assign opacity by length of categories
            opacity = 1 / len(layerCategory)

            # Each data stop unit is a standard deviation
            dataStop = stdev(dataValues)

            # Make 9 data stop values and colors for map gradient
            for i in range(9):
                stp = min(dataValues) + (dataStop * i)

                if reverseColors:
                    col = hexList[(8 - i)]
                else:
                    col = hexList[i]

                stops.append([stp, col])

        # Compile dictionary for output
        output.append(
            {
                "*name*": nickName,
                "*shownByDefault*": enabledByDefault,
                "*ref*": "data/{}.geojson".format(origin),
                "category": category,
                "colorsReversed": reverseColors,
                "displayOrder": displayOrder,
                "*layerSpec*": {
                    "ID_name": ID_name,
                    "*id*": dataField,
                    "*source*": dataField,
                    "*type*": "fill",
                    "*paint*": {
                        "fill-color": {"*property*": dataField, "*stops*": stops,},
                        "fill-opacity": opacity,
                    },
                    "*filter*": ["==", "$type", "Polygon"],
                },
            }
        )

        return dataField

    def producePointsLayer(layerCategory, layer):

        # Get metadata for each field from metadata dictionary entry
        dataField = layer["dataField"]
        origin = layer["origin"]
        category = layer["categoryInfo"]["name"]
        displayOrder = layer["categoryInfo"]["displayOrder"]
        nickName = layer["nickName"]
        reverseColors = layer["reverseColors"]
        ID_name = layer["ID_name"]
        enabledByDefault = layer["enabledByDefault"]

        output.append(
            {
                "*name*": nickName,
                "*shownByDefault*": enabledByDefault,
                "*ref*": "data/{}.geojson".format(origin),
                "category": category,
                "colorsReversed": reverseColors,
                "displayOrder": displayOrder,
                "*layerSpec*": {
                    "ID_name": ID_name,
                    "*id*": dataField,
                    "*type*": "circle",
                    "*source*": dataField,
                    "*paint*": {
                        "circle-radius": {
                            "*base*": 1.75,
                            "*stops*": [[12, 2.7], [22, 180]],
                        },
                        "circle-color": "#111",
                    },
                },
            }
        )

        return dataField

    # Run main function when called
    main()
