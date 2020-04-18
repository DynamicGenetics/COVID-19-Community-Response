import json

geoLabelsToIgnore = ['objectid', 'bng_e', 'bng_n']

def generateLayer(dataSources, nicknames, filename_output):
    dictionary={}
    data=[]
    output=[]
    exceptions=[]
    origins={}
    id_count=0
    categories={}

    opacity = 2/len(dataSources)
    type_filter = 'Polygon'

    #data/{}.geojson'.format(data['name']

    for src in dataSources:
        try:
            filename = 'data/{}.geojson'.format(src['name'])
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
                                    origins[dataField]=src['name']
                                    categories[dataField]=src['category']
                                else:
                                    dictionary[dataField]=[]
                                    dictionary[dataField].append(dataValue)
                                    origins[dataField]=src['name']
                                    categories[dataField]=src['category']
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
            continue

    #print(data)
    # Build output dictionary for JSON layer production AFTER establishing min/maxes
    
    for dataField in data:
        #print("dataField for output", dataField)
        name=dataField['dataField']
        category = categories[dataField['dataField']]

        stops = []
        count=0

        #compute stops and colors (given color)
        for _ in range(8):
            stp = dataField['dataStops']*count

            if category == 'covid':
                col = 'rgb({},125,125)'.format(255/9*count)
            elif category == 'community':
                col = 'rgb(125,{},125)'.format(255/9*count)
            elif category == 'bias':
                col = 'rgb(125,125,{})'.format(255/9*count)

            stops.append([stp,col])
            count+=1

        try:
            nickNm = nicknames[name]

            output.append({
                "*name*": nickNm,
                "*shownByDefault*": False,
                "*ref*": '../data/{}.geojson'.format(origins[name]),
                "*layerSpec*": {
                    "*id*": name,
                    "*source*": name, #origins[name]
                    "*type*": 'fill',
                    "*paint*": {
                        'fill-color': {
                            "*property*": name,
                            "*stops*": stops
                        },
                        'fill-opacity': opacity
                    },
                    "*filter*": ['==', '$type', type_filter]
                },
            })

        except:
            #print("Warning (generateLayer): Property has no nickname and so was skipped for output: ", name)
            exceptions.append(name)
            continue


        id_count+=1
    
    with open(filename_output, 'w') as outs:
        #jsonDumps = json.dump(output, indent=4, sort_keys=True)
        outs.write('var layers={}'.format(output))
    
    return("Message (generateLayers): Layers produced: {}. Exceptions: {}".format(len(output),exceptions))