from __future__ import print_function
import json

geoLabelsToIgnore = ['objectid', 'bng_e', 'bng_n']

def generateLayer(dataSources, filename_output):
    dictionary={}
    data=[]
    output=[]
    exceptions=[]
    origins={}
    categories={}
    categoryCount={}
    nicknames={}
    points=[]
    reversedLayers={}

    #opacity = 1/len(dataSources)
    type_filter = 'Polygon'

    #data/{}.geojson'.format(data['name']

    for src in dataSources:

        try: categoryCount[src['category']]+=1
        except: categoryCount[src['category']]=1

        try:

            if src['geometry'] == 'Points':
                print("Message (generateLayers): Point layer identified ({})".format(src['name']))
                points.append(src['name'])
                origins[src['name']]=src['name'].replace("_points","")
                categories[src['name']]=src['category']
                nicknames[src['name']]=src['layers'][src['name']]
                continue
            
            else:
                filename = 'data/{}.geojson'.format(src['name'])
                with open(filename, 'r') as geojson_file:

                        geojson = json.load(geojson_file)

                        # For row in geoJSON, count values and assign color values
                        for feature in geojson["features"]:

                            properties = feature["properties"]

                            for dataField in properties.keys():

                                #If dataField in dataSource found AND not disabled then process further
                                if dataField in src['layers'].keys(): 
                                    if src['layers'][dataField] != 'DISABLED':

                                        dataValue = properties[dataField]

                                        if dataField in dictionary.keys():
                                            dictionary[dataField].append(dataValue)
                                            origins[dataField]=src['name']
                                            categories[dataField]=src['category']
                                            nicknames[dataField]=src['layers'][dataField]
                                            reversedLayers[src['name']]=src['reverseColors']
                                            
                                        else:
                                            dictionary[dataField]=[]
                                            dictionary[dataField].append(dataValue)
                                            origins[dataField]=src['name']
                                            categories[dataField]=src['category']
                                            nicknames[dataField]=src['layers'][dataField]
                                            reversedLayers[dataField]=src['reverseColors']
                                    
                                    else: exceptions.append('{}(disabled)'.format(dataField))
                                else: 
                                    exceptions.append(dataField)
                                    #print("ERROR (generateLayer): datafield found in dataSource not specified in dataSources")
                                
        except:
            #print("ERROR w/ reading data sources.py for src: ", filename)
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
        #print(dataField)
        #print("dataField for output", dataField)
        name=dataField['dataField']
        category = categories[dataField['dataField']]

        stops = []

        colorHexes = {
            'yellow-blue':['#f7fcf0','#e0f3db','#ccebc5','#a8ddb5','#7bccc4','#4eb3d3','#2b8cbe','#0868ac','#084081'],
            'yellow-red':[ '#fff7ec','#fee8c8','#fdd49e','#fdbb84','#fc8d59','#ef6548','#d7301f','#b30000','#7f0000'],
            'yellow-green':['#ffffe5','#f7fcb9','#d9f0a3','#addd8e','#78c679','#41ab5d','#238443','#006837','#004529']
        }

        #try:
        nickNm = nicknames[name]

        # Compute stops and colors (given color)
        for i in range(8):
            stp = dataField['dataStops']*(i+1)

            if category == 'covid':
                hexList = colorHexes['yellow-blue']
            elif category == 'community':
                hexList = colorHexes['yellow-green']
            elif category == 'bias':
                hexList = colorHexes['yellow-red']
            else: print("ERROR (generateLayer): Layer has no category")
            
            if reversedLayers[name]==True: hexList.reverse()
            
            col = hexList[i]

            stops.append([stp,col])
            opacity = 1/categoryCount[categories[name]]

        # Compile dicts for output
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

        #except:
        #    #print("Warning (generateLayer): Property has no nickname and so was skipped for output: ", name)
        #    exceptions.append(name)

    for dataField in points:
        #print(dataField)
        try:
            name = dataField
            nickNm = nicknames[name]
            
            output.append({
                "*name*": nickNm,
                "*shownByDefault*": False,
                "*ref*": '../data/{}.geojson'.format(origins[name]),
                "*layerSpec*": {
                    "*id*": name,
                    "*type*": 'circle',
                    "*source*": name,
                    "*paint*": {
                        'circle-radius': {
                            "*base*": 1.75,
                            "*stops*": [[12, 2.7], [22, 180]]
                        },
                        'circle-color': '#111'
                    }
                }
            })

        except:
            exceptions.append(name)
    
    with open(filename_output, 'w') as outs:
        jsonDumps = json.dumps(output, indent=4, sort_keys=True)
        outs.write('var layers={}'.format(jsonDumps))
    
    return("Message (generateLayers): Layers produced: {}. Exceptions: {}".format(len(output),set(exceptions)))