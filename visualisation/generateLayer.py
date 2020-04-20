from dataSources import LAYERCOLORS as colorHexes
import json

geoLabelsToIgnore = ["objectid", "bng_e", "bng_n"]


def generateLayer(dataSources, filename_output):
    output = []
    exceptions = []
    layers = {}

    # opacity = 1/len(dataSources)
    type_filter = "Polygon"

    # data/{}.geojson'.format(data['name']

    for src in dataSources:

        try:

            if src["geometry"] == "Points":

                for dataField in src["layers"].keys():
                    layer = src["layers"][dataField]

                    if not layer["disabled"]:

                        if layer["category"] not in layers.keys():
                            layers[layer["category"]] = {}

                        layers[layer["category"]][dataField] = {
                            "dataField": dataField,
                            "origin": src["name"],
                            "path": src["path"],
                            "category": layer["category"],
                            "nickName": layer["nickName"],
                            "reverseColors": layer["reverseColors"],
                            "geometry": src["geometry"],
                            "values": None,
                            "ID_name": src["ID_name"],
                            "enabledByDefault": layer["enabledByDefault"],
                        }

            else:
                filename = "data/{}.geojson".format(src["name"])
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

                                    if layer["category"] not in layers.keys():
                                        layers[layer["category"]] = {}

                                    if (
                                        dataField
                                        not in layers[layer["category"]].keys()
                                    ):
                                        layers[layer["category"]][dataField] = {
                                            "dataField": dataField,
                                            "origin": src["name"],
                                            "path": src["path"],
                                            "category": layer["category"],
                                            "nickName": layer["nickName"],
                                            "reverseColors": layer["reverseColors"],
                                            "geometry": src["geometry"],
                                            "dataValues": [dataValue],
                                            "ID_name": src["ID_name"],
                                            "enabledByDefault": layer[
                                                "enabledByDefault"
                                            ],
                                        }
                                    else:
                                        layers[layer["category"]][dataField][
                                            "dataValues"
                                        ].append(dataValue)

                                    # print("dataField: {}, origins: {}, categories: {}, nickNames: {}, reversedLayers: {}".format(dataField,origins,categories,nickNames,reversedLayers))

                                else:
                                    exceptions.append("{}(disabled)".format(dataField))

                            else:
                                exceptions.append(dataField)
                                # print("ERROR (generateLayer): datafield found in dataSource not specified in dataSources")

        except:
            # print("ERROR w/ reading data sources.py for src: ", filename)
            exceptions.append(filename)

    o = 0
    # First process polygon data
    for key_category in layers:
        layerCategory = layers[key_category]

        # Assign colors to categories
        opacity = 1 / len(layerCategory)
        hexList = colorHexes[o]

        for key_layer in layerCategory:
            layer = layerCategory[key_layer]

            # Get properties of layers under category
            dataField = layer["dataField"]
            origin = layer["origin"]
            category = layer["category"]
            nickName = layer["nickName"]
            reverseColors = layer["reverseColors"]
            geometry = layer["geometry"]
            ID_name = layer["ID_name"]
            enabledByDefault = layer["enabledByDefault"]

            # try:

            if geometry == "Polygons":

                dataValues = layer["dataValues"]
                stops = []

                # Get range of each property dataField in geoJSON (for numerical polygon data only) & compute stops / colors
                if isinstance(dataValues[0], int) or isinstance(dataValues[0], float):

                    dataStop = (max(dataValues) - min(dataValues)) / 8

                    for i in range(9):
                        stp = min(dataValues) + (dataStop * i)

                        if reverseColors:
                            col = hexList[(8 - i)]
                        else:
                            col = hexList[i]

                        stops.append([stp, col])

                # Compile dicts for output
                output.append(
                    {
                        "*name*": nickName,
                        "*shownByDefault*": enabledByDefault,
                        "*ref*": "../data/{}.geojson".format(origin),
                        "category": category,
                        "colorsReversed": reverseColors,
                        "*layerSpec*": {
                            "ID_name": ID_name,
                            "*id*": dataField,
                            "*source*": dataField,
                            "*type*": "fill",
                            "*paint*": {
                                "fill-color": {
                                    "*property*": dataField,
                                    "*stops*": stops,
                                },
                                "fill-opacity": opacity,
                            },
                            "*filter*": ["==", "$type", type_filter],
                        },
                    }
                )

            # Now process point data
            elif layer["geometry"] == "Points":

                output.append(
                    {
                        "*name*": nickName,
                        "*shownByDefault*": enabledByDefault,
                        "*ref*": "../data/{}.geojson".format(origin),
                        "category": category,
                        "colorsReversed": reverseColors,
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

            #    except:
            #        exceptions.append(dataField)

        # print("Processed category: ", key_category)
        o += 1

    with open(filename_output, "w") as outs:
        jsonDumps = json.dumps(output, indent=4, sort_keys=True)
        outs.write("var layers={}".format(jsonDumps))

    return "Message (generateLayers): Layers produced: {}. Exceptions: {}".format(
        len(output), set(exceptions)
    )
