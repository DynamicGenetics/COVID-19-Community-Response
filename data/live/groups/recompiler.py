import csv  
import json  
import re
from shapely.geometry import shape, Point

URLs={}

def convertGroups(filename_boundaries_wales, filename_boundaries_LA, filename_csv, filename_demographics, filename_output_groups, filename_output_groupCount, filename_output_URLs, filename_output_review):

    #Import welsh boundaries
    # load GeoJSON file containing sectors
    wales_identified = False
    with open(filename_boundaries_wales) as boundaries:
        boundaries_js = json.load(boundaries)

        features = boundaries_js['features']
        for feature in features:
            properties = feature["properties"]
            if properties["ctry19cd"] == "W92000004":
                polygon = shape(feature['geometry'])
                wales_identified = True
                print("BOUNDARY GEOJSON: Welsh borders found and imported.")

    # load GeoJSON file containing sectors
    LA_polygons = []
    LAs_identified = 0
    welshLAs=[]
    with open(filename_boundaries_LA) as LAs:
        LAs_js = json.load(LAs)

        features = LAs_js['features']
        for feature in features:
            properties = feature["properties"]    

            #Convert long/lat strings into numbers
            long = float(properties["long"])
            lat = float(properties["lat"])
            #Construct point from coords
            point = Point(long,lat)

            #Check polygon for Wales to see if it contains the point
            if polygon.contains(point):

                welshLAs.append(feature)

                print ('LA boundary found within polygon:', point)
                LAs_identified+=1
                LA_polygons.append({
                                        "lad18nm": properties["lad18nm"], 
                                        "lad18cd": properties["lad18cd"], 
                                        "LA_shape": shape(feature['geometry']),
                                        "LA_groupCount": 0,
                                        "LA_groups":[]
                                     })

    # Open the demographics CSV  
    with open(filename_csv, newline='', encoding='utf-8') as f:

        print("OPENING groups CSV: ", filename_csv)
        # Initialise reader
        groups_QC = csv.DictReader( f, fieldnames = ("Location","Lat","Lng","Title","URL","Display","Source","Notes"))
        #groups_unfiltered
        #groups_QC = QCFilter(groups_unfiltered, "QC/groupsSampleReviewed.csv")
        
        #Initialise variables
        groups=[]
        welshGroups=0
        nonWelshGroups=0
        exceptions=0
        exceptions_names=[]
        display0=0
        rowCount=0
        pointsInLAs=0
        geomWelshGrps=[]
        duplicates=0

        # Build json from csv
        for row in groups_QC:

            rowCount+=1

            #Skip row if header
            if row["Title"] == "Title":
                continue 
                
            #Skip row if set not to display         
            if row["Display"] == "FALSE":
                display0+=1
                continue 
                
            else:
                try:
                    print("Compiling geoJSON: ", row["Title"])

                    #Convert long/lat strings into numbers
                    long = float(row["Lng"])
                    lat = float(row["Lat"])

                    #Construct point from coords
                    point = Point(long,lat)

                    #Check polygon for Wales to see if it contains the point
                    if polygon.contains(point):
                        print ('Found containing polygon:', point)  

                        geoJSON = {
                                    "type":"Feature",
                                    "geometry":{
                                        "type":"Point",
                                        "coordinates":[long, lat]
                                        },
                                    "properties": {
                                        "Location" : row["Location"],
                                        "Title" : row["Title"],
                                        "URL" : row["URL"],
                                        "Display" : row["Display"],
                                        "Source" : row["Source"],
                                        "Notes": row["Notes"]
                                     }
                                  }

                        welshGroups+=1
                        groups.append(geoJSON)
                    else:
                        nonWelshGroups+=1

                    for LA in LA_polygons:
                        if LA["LA_shape"].contains(point):

                            if detectDuplicate(LA["lad18cd"], row["URL"]) == False:
                                geomWelshGrps.append([row["Location"],row["Title"],LA["lad18nm"], LA["lad18cd"], row["URL"], row["Notes"]])

                                print("Point located in LA", point)
                                LA["LA_groupCount"]+=1
                                LA["LA_groups"].append(row["Title"])
                                pointsInLAs+=1

                            else:
                                duplicates+=1
                                print("Duplicate detected and excluded: ", row)

                except:
                    print("EXCEPTION. Unable to process: ", row["Title"])
                    exceptions+=1
                    exceptions_names.append(row["Title"])
                    continue        
    
    
    #Count groups per area
    
    output=[]
    with open(filename_demographics, newline='', encoding='utf-8') as f:

        print("OPENING demographics CSV: ", filename_demographics)
        reader = csv.DictReader( f, fieldnames = ("la","id_area","deprivation_30","pop","pop_density","pop_elderly","lhb","language","covid"))

        demographics={} 
        
        # Build JSON dictionary for demographics
        
        for LA in welshLAs:

            properties = LA["properties"]
            print("Synthesising: ", properties["lad18cd"])
            #print("Start props: ", properties)
            for row in reader:
                if properties["lad18cd"] == row["id_area"]:  
                    print("Row found: ", properties["lad18cd"])
                    lad18cd = properties["lad18cd"]
                    pop = float(row["pop"].replace(",","",))
                    pop_elderly = float(row["pop_elderly"].replace(",","",))
                    break

            for LA in LA_polygons:
                if properties["lad18cd"] == LA["lad18cd"]: 
                    print("LA polygon match: ", LA["lad18cd"])
                    groupCount = LA["LA_groupCount"]
                    groupCount_pop = groupCount / pop
                    groupCount_elderly = groupCount / (pop_elderly / 100 * pop)
                    break

            #print("Final properties: ", lad18cd, pop, pop_elderly, groupCount)

            properties["lad18cd"] = lad18cd
            properties["groupCount"] = groupCount
            properties["groupCount_pop"] = groupCount_pop
            properties["groupCount_elderly"] = groupCount_elderly

            #print(properties)
            output.append(LA)
            
            #Save output
            saveOutput(groups, output, geomWelshGrps, filename_output_groups, filename_output_groupCount, filename_output_URLs, filename_output_review)
            
            
    #Finished
    print("#####################################################")
    print("100% COMPLETE")
    print("#####################################################")
    print("################ GEOGRAPHICAL BORDERS ###############")
    print("WELSH BORDER IDENTIFIED: ", wales_identified)
    print("NUMBER OF LA BOUNDARIES IDENTIFIED: ", LAs_identified)
    print("############## COMMUNITY SUPPORT GROUPS #############")
    print("TOTAL: ", rowCount)
    print("WELSH: ", welshGroups)
    print("NON-WELSH :", nonWelshGroups)
    print("EXCLUDED (Display: FALSE in csv): ", display0)
    print("DUPLICATES: ", duplicates)
    print("EXCEPTIONS / ERRs: ", exceptions)
    print("GROUPS THROWING ERRORS: ", exceptions_names)
    print("################### COUNT PER LA ##################")
    print("LAs: ", len(LA_polygons))
    print("GROUPS LOCALISED TO LAs: ", pointsInLAs)
    print("LAs in output: ", len(output))
    print("#####################################################")
    

def detectDuplicate(LA, URL):
    
    #Find root URL
    if re.search('facebook', URL):
        
        print("facebook URL found: ", URL)
        
        if re.search('groups/', URL):
            fbGroupId = URL.split('groups/')[1]
            fbGroupId_tail = re.search('/',fbGroupId)

            if fbGroupId_tail:
                standardisedLink = fbGroupId.split('/')[0]
                print(standardisedLink)

            else:
                standardisedLink = fbGroupId
                print(standardisedLink)
                
        elif re.search('facebook.com/', URL): 
            standardisedLink = URL.split('facebook.com/')[1]
            print(standardisedLink)
        
        else: 
            standardisedLink = URL 
            print(standardisedLink)
    else:
        standardisedLink = URL
        print(standardisedLink)
    
    if LA not in URLs:
        URLs[LA]=[]
        return(False)
    elif standardisedLink in URLs[LA]:
        return(True)
    else:
        URLs[LA].append(standardisedLink)
        return(False)    
    
def saveOutput(groups, output, geomWelshGrps, filename_output_groups, filename_output_groupCount, filename_output_URLs, filename_output_review):      

    #Write to geojson
    geoJSON_groups = {"type": "FeatureCollection", "features": groups}
    with open(filename_output_groups, 'w') as grps:
       json.dump(geoJSON_groups, grps)

    geoJSON_groupsCount = {"type": "FeatureCollection", "features": output}
    with open(filename_output_groupCount, 'w') as grpsC:
       json.dump(geoJSON_groupsCount, grpsC)
    
    #Write URLs to json
    with open(filename_output_URLs, 'w') as urls:
       json.dump(URLs, urls)

    #To CSV Operation
    f = open(filename_output_review, 'w', encoding='utf-8', newline="")

    with f:

        writer = csv.writer(f)

        for row in geomWelshGrps:
            writer.writerow(row)