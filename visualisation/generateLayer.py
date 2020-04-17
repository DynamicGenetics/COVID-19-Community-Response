import json

geoLabelsToIgnore = ['objectid', 'bng_e', 'bng_n']

def generateLayer(filenames, color, filename_output):
    dictionary={}
    data=[]
    output=[]
    exceptions=[]
    origins={}

    opacity = 1/len(filenames)
    type_filter = 'Polygon'

    for filename in filenames:
        try:
            with open(filename, 'r') as geojson_file:

                    geojson = json.load(geojson_file)

                    # For row in geoJSON, count values and assign color values
                    for feature in geojson["features"]:

                        properties = feature["properties"]

                        for dataField in properties.keys():

                            if dataField not in geoLabelsToIgnore: 
                                dataValue = properties[dataField]

                                if dataField in dictionary.keys():
                                    dictionary[dataField].append(dataValue)
                                    origins[dataField]=filename
                                else:
                                    dictionary[dataField]=[]
                                    dictionary[dataField].append(dataValue)
                                    origins[dataField]=filename
        except:
            #print("COULDN't find file", filename)
            exceptions.append(filename)

    # Get range of each property dataField in geoJSON
    for dataField in dictionary.keys():
        dataValues = dictionary[dataField]
        
        if isinstance(dataValues[0], int) or isinstance(dataValues[0], float):
            #print("int found: ", dataField)
            data.append({
                'dataField' : dataField,
                'dataStops' : (max(dataValues) - min(dataValues))/9
            })
        else:
            continue;

    #print(data)
    # Build output dictionary for JSON layer production AFTER establishing min/maxes
    
    for dataField in data:
        #print("dataField for output", dataField)
        name=dataField['dataField']
        stp=dataField['dataStops']

        output.append({
            'name': name,
            'shownByDefault': False,
            'layerSpec': {
                'id': name,
                'type': 'fill',
                'source': origins[name],
                'paint': {
                    'fill-color': {
                        'property': name,
                        'stops': [[stp*1, 'rgb({},0,0)'.format(256/9*1)],
                                [stp*2, 'rgb({},0,0)'.format(256/9*2)],
                                [stp*3, 'rgb({},0,0)'.format(256/9*3)],
                                [stp*4, 'rgb({},0,0)'.format(256/9*4)],
                                [stp*5, 'rgb({},0,0)'.format(256/9*5)],
                                [stp*6, 'rgb({},0,0)'.format(256/9*6)],
                                [stp*7, 'rgb({},0,0)'.format(256/9*7)],
                                [stp*8, 'rgb({},0,0)'.format(256/9*8)],
                                [stp*9, 'rgb({},0,0)'.format(256/9*9)]]
                    },
                    'fill-opacity': opacity
                },
                'filter': ['==', '$type', type_filter]
            },
        })
    
    with open(filename_output, 'w') as outs:
      json.dump(output, outs, indent=4, sort_keys=True)

    
    return("Message (generateLayers): Layers produced: {}. Exceptions: {}".format(len(output),exceptions))