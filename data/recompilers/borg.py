import json
import csv

def assimilate(csvFile, geojsonFile, rownames, idHeadName):
    
    #Import files
    
    with open(geojsonFile) as boundaryFile:
        boundaries = json.load(boundaryFile)
    
    with open(csvFile, newline='', encoding='utf-8') as dataFile:
        csvData = csv.DictReader(data_CSV, fieldnames = rownames)
    
    
    #Assimilate properties in csv into geojson
    
    for LSOA in boundaries:
        print(LSOA)
        
        properties = LSOA["properties"]
        print("Synthesising: ", properties["lad18cd"])        
        
        for row in csvData:
        
            if properties["lad18cd"] == row['lad18cd']: 
                
            for name in rownames:
       
            

                print("Row found: ", properties["lad18cd"])
                lad18cd = properties["lad18cd"]
                cases_total = float(row['Cumulative  cases'].replace(" ","",))
                break  

        print("Final properties: ", lad18cd, cases_total)
        
        properties["cases_total"] = cases_total    
        output.append(LSOA)
    
    #Export output
    geoJSON_cases = {"type": "FeatureCollection", "features": output}
    with open('../{}.geoJSON'.format(filename.replace("csv", ""), 'w')) as cses:
           json.dump(geoJSON_groups, grps)
            
def deconstruct(geojson):
    pass