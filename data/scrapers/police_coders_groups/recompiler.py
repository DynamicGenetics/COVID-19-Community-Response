import csv
import json
from shapely.geometry import shape, Point
from data.community_measures.QC.detectDuplicate import detectDuplicate
from data.community_measures.QC.QC import QCFilter


# Initialise variables
groups = []
welshGroups = 0
nonWelshGroups = 0
exceptions = 0
exceptions_names = []
display0 = 0
pointsInLAs = 0
geomWelshGrps = []
duplicates = 0
unacceptableDisplayCodes = ["DUPLICATE", "NOT GROUP", "NOT LOCAL"]

def groupProcessing(filenames, boundaryfile):

    URLs = {}

    filename_boundaries_wales = filenames["boundaries_wales"]
    filename_boundaries_LA = filenames["boundaries_LA"]
    filename_csv = filenames["csv"]
    filename_demographics = filenames["demographics_legacy"]

    varNm_geog_areaID =  boundaryfile['ID_name']
    varNm_geog_areaNm = boundaryfile['area_name']
    
    polygon=getWelshBoundary()

    features=getLSOABoundaries()

    filteredList=filterBoundariesByWelsh(features, polygon)
    LA_polygons=filteredList['filtered area polygons']
    welshLAs=filteredList['filtered area features']

    groups_QC=getQualityControlledList()

    enterGroupsAsFeatures()

    demographics=getDemographics()

    output = countGroupsPerArea()

    print("Message (groupProcessing): {} groups identified".format(pointsInLAs))

    return (groups, output, geomWelshGrps, URLs)

# Import welsh boundaries
def getWelshBoundary():
    
    # load GeoJSON boundary file
    wales_identified = False
    with open(filename_boundaries_wales) as boundaries:
        boundaries_js = json.load(boundaries)

        features = boundaries_js["features"]
        for feature in features:
            properties = feature["properties"]
            if properties["ctry19cd"] == "W92000004":
                polygon = shape(feature["geometry"])

    return(polygon)

# Import LSOA boundaries
def getLSOABoundaries():
    features=[]

    with open(filename_boundaries_LA) as LAs:
        LAs_js = json.load(LAs)

    for feature in LAs_js["features"]:
        if feature[""]

        features = LAs_js

    return(features)


def filterBoundariesByWelsh(features, polygon):

    # load welsh LSOAs only from LSOA boundary file
    LA_polygons = []
    welshLAs = []

    for feature in features:
        properties = feature["properties"]

        # Construct point from coords
        point = shape(feature["geometry"]).representative_point()
        #print(point)

        # Check polygon for Wales to see if it contains the point
        if polygon.contains(point):
            
            LA_polygons.append(
                {
                    "area_name": properties[varNm_geog_areaNm],
                    "areaID": properties[varNm_geog_areaID],
                    "LA_shape": shape(feature["geometry"]),
                    "LA_groupCount": 0,
                    "LA_groups": [],
                }
            )

            welshLAs.append(feature)

    return({'filtered area polygons' : LA_polygons, 'filtered area features' : welshLAs})

# def duplicateTest():
#    return()

# def getQualityControlledList():
#     QCdict = {}
#     with open(filename_csv, newline="", encoding="utf-8") as f:
#         groups_QC = csv.DictReader(f)
#         for row in groups_QC:
#             if row["Display"] in unacceptableDisplayCodes:
#             QCdict[row["Title"]] = row["Display"]
#     return(QCdict)

def enterGroupsAsFeatures(groups_QC, polygon):

    # Build json from csv
    for row in groups_QC:
        
        # Skip row if header
        if row["Title"] == "Title":
            continue

        # Convert long/lat strings into numbers
        long = float(row["Lng"])
        lat = float(row["Lat"])

        # Construct point from coords
        point = Point(long, lat)

        # Check polygon for Wales to see if it contains the point
        if polygon.contains(point):

            geoJSON = {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [long, lat]},
                "properties": {
                    "Location": row["Location"],
                    "Title": row["Title"],
                    "URL": row["URL"],
                    "Display": row["Display"],
                    "Source": row["Source"],
                    "Notes": row["Notes"],
                },
            }

            groups.append(geoJSON)

        for LA_ply in LA_polygons:
            if LA_ply["LA_shape"].contains(point):

                duplicateTest = detectDuplicate(
                    LA_ply["areaID"], row["URL"], URLs
                )

                if duplicateTest[0] == False:
                    geomWelshGrps.append(
                        [
                            row["Location"],
                            row["Title"],
                            LA_ply["area_name"],
                            LA_ply["areaID"],
                            row["URL"],
                            row["Notes"],
                        ]
                    )

                    LA_ply["LA_groupCount"] += 1
                    LA_ply["LA_groups"].append(row["Title"])
                    pointsInLAs += 1
                    URLs = duplicateTest[1]

                else:
                    duplicates += 1

# Build dictionary for demographics
def getDemographics():
    demographics = {}
    
    with open(filename_demographics, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:

            demographics[row["areaID"]] = {
                "pop": float(row["WIMD_rank"].replace(",", "",)),
                "pop_elderly": float(row["language"].replace(",", "",)),
            }

    return(demographics)

# Count groups per area
def countGroupsPerArea():
    output = []
    for LA in welshLAs:
        properties = LA["properties"]
        areaID_name = properties[varNm_geog_areaID]
        pop = demographics[areaID_name]["pop"]
        pop_elderly = demographics[areaID_name]["pop_elderly"]

        # print('LA:', lad18cd, pop, pop_elderly)

        for LA_p in LA_polygons:
            if areaID_name == LA_p["areaID"]:
                groupCount = LA_p["LA_groupCount"]
                groupCount_pop = groupCount / pop
                groupCount_elderly = groupCount / (pop_elderly / 100 * pop)
                # print("MATCH: LA_p: ",areaID_name, LA_p["lad18cd"])
                break
            else:
                continue

        #print("LA:", lad18cd, groupCount, groupCount_pop, groupCount_elderly)

        properties["groupCount"] = groupCount
        properties["groupCount_pop"] = groupCount_pop
        properties["groupCount_elderly"] = groupCount_elderly

        # print("output",lad18cd)
        output.append(LA)
    return(output)