import csv  
import json  
        
# Open the demographics CSV  
with open('demographics.csv', newline='', encoding='utf-8') as f:
    
    print("OPENING CSV: demographics.csv")
    # Initialise reader
    reader = csv.DictReader( f, fieldnames = ("la","id_area","deprivation_30","pop","pop_density","pop_elderly","lhb","language","covid"))
    
    demographics={}    
    # Build JSON dictionary for demographics
    for row in reader:
        
        if row["id_area"] == "id_area":
            continue
        else:
            print("Processing: ", row["id_area"])
        
        properties={
            "id_area" : row["id_area"], 
            "deprivation_30" : float(row["deprivation_30"].replace(",","",)),
            "pop_density" : float(row["pop_density"].replace(",","",)),
            "pop" : float(row["pop"].replace(",","",)),
            "pop_elderly" : float(row["pop_elderly"].replace(",","",)),
            "lhb" : row["lhb"],
            "language" : float(row["language"].replace(",","",)),
            "covid": float(row["covid"].replace(",","",))
        }
        
        demographics[row["id_area"]]=properties

        
#Initialise dictionary object for area boundaries
boundaries={}
# Open the boundaries geojson
with open('../../boundaries_LSOAs.geojson', 'r') as json_file:
    
    print("OPENING GEOJSON: boundaries.geojson")
    data = json.load(json_file)
    
    for row in data["features"]:
        
        properties = row["properties"] 
        
        row["properties"]=demographics[properties["lad18cd"]]
        
        
#Finished
print("PROCESS COMPLETE")

with open('../../demographics.geojson', 'w') as demos:
   json.dump(data, demos)
