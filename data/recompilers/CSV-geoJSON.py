import json
import csv

def csvToGeojson(csv, geojson):

    with open(geojson) as boundaryFile:
            boundaries = json.load(boundaryFile)
    
    with open(csv, newline='', encoding='utf-8') as data_CSV:
            data = csv.DictReader(data_CSV)

    output=[]
    for LHB in LHBs:
        print(LSOA)
        properties = LSOA["properties"]

        print("Synthesising: ", properties["lad18cd"])
        print("Start props: ", properties)

        for row in cases:
            if properties["lad18cd"] == healthboards[row['Health  Board']]['onsName']: 

                print("Row found: ", properties["lad18cd"])
                lad18cd = properties["lad18cd"]
                cases_total = float(row['Cumulative  cases'].replace(" ","",))
                break  

        print("Final properties: ", lad18cd, cases_total)

        properties["cases_total"] = cases_total    
        output.append(LSOA)
    
    geoJSON_cases = {"type": "FeatureCollection", "features": output}
    with open('../{}.geoJSON'.format(filename.replace("csv", ""), 'w')) as cses:
           json.dump(geoJSON_groups, grps)