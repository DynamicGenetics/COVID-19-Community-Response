import csv  
import json  
import re
from shapely.geometry import shape, Point

URLs={}

def convertGroups(filenames):

    filename_boundaries_wales = filenames["boundaries_wales"]
    filename_boundaries_LA = filenames["boundaries_LA"] 
    filename_csv = filenames["csv"] 
    filename_demographics = filenames["demographics_legacy"] 

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

                #print ('LA boundary found within polygon:', point)
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
        groups_QC = csv.DictReader(f)
        
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
        unacceptableDisplayCodes=["Duplicate", "Not Group", "Not Local"]

        # Build json from csv
        for row in groups_QC:

            rowCount+=1

            #Skip row if header
            if row["Title"] == "Title":
                continue 
                
            #Skip row if set not to display         
            elif row["Display"] in unacceptableDisplayCodes:
                display0+=1
                continue 
                
            else:
                # try:
                #print("Compiling geoJSON: ", row["Title"])

                #Convert long/lat strings into numbers
                long = float(row["Lat"])
                lat = float(row["Lng"])

                #Construct point from coords
                point = Point(long,lat)

                #Check polygon for Wales to see if it contains the point
                if polygon.contains(point):
                    #print ('Found containing polygon:', point)  

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

                    for LA_ply in LA_polygons:
                        if LA_ply["LA_shape"].contains(point):
                            
                            print("CONTAINSCONTAINSCONTIAN")

                            if detectDuplicate(LA_ply["lad18cd"], row["URL"]) == False:
                                geomWelshGrps.append([row["Location"],row["Title"],LA_ply["lad18nm"], LA_ply["lad18cd"], row["URL"], row["Notes"]])

                                #print("Point located in LA_ply", point)
                                LA_ply["LA_groupCount"]+=1
                                LA_ply["LA_groups"].append(row["Title"])
                                pointsInLAs+=1

                            else:
                                duplicates+=1
                                #print("Duplicate detected and excluded: ", row)

                # except:
                #     print("EXCEPTION. Unable to check if polygon cotnains point: ", row["Title"])
                #     exceptions+=1
                #     exceptions_names.append(row["Title"])
                #     continue        

    
    #Count groups per area
    
    output=[]
    with open(filename_demographics, newline='', encoding='utf-8') as f:

        print("OPENING demographics CSV: ", filename_demographics)
        reader = csv.DictReader(f)

        demographics={} 
        
        # Build JSON dictionary for demographics
        for LA in welshLAs:
            print("len LA before: ", len(LA))
            print("keys LA before: ", LA.keys())
            properties = LA["properties"]
            #print("Synthesising: ", properties["lad18cd"])
            #print("Start props: ", properties)
            for row in reader:
                if properties["lad18cd"] == row["id_area"]:  
                    #print("Row found: ", properties["lad18cd"])
                    lad18cd = properties["lad18cd"]
                    pop = float(row["pop"].replace(",","",))
                    pop_elderly = float(row["pop_elderly"].replace(",","",))
                    break
            print("len LA_polygons: ", len(LA_polygons))

            for LA_p in LA_polygons:
                if properties["lad18cd"] == LA_p["lad18cd"]: 
                    #print("LA polygon match: ", LA["lad18cd"])
                    groupCount = LA_p["LA_groupCount"]
                    groupCount_pop = groupCount / pop
                    groupCount_elderly = groupCount / (pop_elderly / 100 * pop)
                    break
            
            print("len LA after: ", len(LA))
            print("keys LA after: ", LA.keys())
            #print("Final properties: ", lad18cd, pop, pop_elderly, groupCount)

            properties["lad18cd"] = lad18cd
            properties["groupCount"] = groupCount
            properties["groupCount_pop"] = groupCount_pop
            properties["groupCount_elderly"] = groupCount_elderly

            #print(properties)
            output.append(LA)
            
    message= [
        ("#####################################################"),
        ("100% COMPLETE"),
        ("#####################################################"),
        ("################ GEOGRAPHICAL BORDERS ###############"),
        ("WELSH BORDER IDENTIFIED: ", wales_identified),
        ("NUMBER OF LA BOUNDARIES IDENTIFIED: ", LAs_identified),
        ("############## COMMUNITY SUPPORT GROUPS #############"),
        ("TOTAL: ", rowCount),
        ("WELSH: ", welshGroups),
        ("NON-WELSH :", nonWelshGroups),
        ("EXCLUDED (Display: FALSE in csv): ", display0),
        ("DUPLICATES: ", duplicates),
        ("EXCEPTIONS / ERRs: ", exceptions),
        ("GROUPS THROWING ERRORS: ", exceptions_names),
        ("################### COUNT PER LA ##################"),
        ("LAs: ", len(LA_polygons)),
        ("GROUPS LOCALISED TO LAs: ", pointsInLAs),
        ("LAs in output: ", len(output)),
        ("#####################################################") 
    ]

    return(groups, output, geomWelshGrps, message)
            
filenames = {
    "boundaries_wales" : "data/geography/boundaries_wales.geoJSON", 
    "boundaries_LA" : "data/geography/boundaries_LAs.geoJSON", 
    "csv" : "data/community_measures/groups.csv", 
    "demographics_legacy" : "data/community_measures/demographics.csv", 
    "output_groups" : "data/groups.geojson", 
    "output_groupCount" : "data/groupCount.geojson", 
    "output_URLs" : "data/community_measures/URLs.json", 
    "output_groupCopyForReview" : "data/community_measures/QC/groupsForReview.csv",
}
groupsData = convertGroups(filenames)
for row in groupsData[3]: print(row)
#saveOutput(groupsData[0], groupsData[1], groupsData[2], filenames)