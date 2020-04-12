import json
import csv

def convertCases(filename):

    with open('../../boundaries_LHBs.GEOJSON') as LHBs_js:
            LHBs = json.load(LHBs_js) 
    
    with open('../../healthboards.json') as LHBs_js:
            healthboards = json.load(LHBs_js) 
    
    with open('cases.csv', newline='', encoding='utf-8') as f:
            cases = csv.DictReader( f, fieldnames = ('Health  Board', 'New cases', 'Cumulative  cases'))

    output=[]
    for LHB in LHBs:
                print(LHB)
                properties = LHB["properties"]

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
                output.append(LHB)
    
    geoJSON_cases = {"type": "FeatureCollection", "features": output}
    with open('../{}.geoJSON'.format(filename.replace("csv", ""), 'w')) as cses:
           json.dump(geoJSON_groups, grps)