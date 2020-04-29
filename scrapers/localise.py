import json
import csv
from shapely.geometry import shape, Point

def iterateGroups(input_path, out_path, fileNm_Wales):
    output = []
    
    polygon = getWelshBoundary(fileNm_Wales)

    with open(input_path, encoding="utf-8") as f:
        data = csv.DictReader(f)

        for row in data:
            point = Point([float(row['Lng']),float(row['Lat'])])

            if polygon.contains(point):

                output.append(row)
            
    with open(out_path, "w", encoding="utf-8") as f:  
        
        writer = csv.writer(f)
        
        #Write csv header
        writer.writerow(row)

        #Write groups as rows
        for row in output:
            writer.writerow(row.values())
    
    print("Message (iterateGroups): Localised {} groups to Wales".format(len(output)))

#Import welsh boundary
def getWelshBoundary(fileNm_Wales):

    with open(fileNm_Wales) as boundaries:
        boundaries_js = json.load(boundaries)

        features = boundaries_js["features"]
        for feature in features:
            properties = feature["properties"]
            
            if properties["ctry19cd"] == "W92000004":
                polygon = shape(feature["geometry"])
    
                return(polygon)