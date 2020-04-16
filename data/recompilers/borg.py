import csv  
import json  

def assimilate(data_type, data_path, data_idName, geo_path, geo_idName, out_path):
    data_toAssimilate={}
    
    #If input is csv
    if data_type == "csv":

        # Open the CSV as dictionary  
        with open(data_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Make dictionary of all columns in csv
            for row in reader:
                properties=[]

                for key in row:

                    try:
                        properties.append((key,float(row[key].replace(",","",))))
                    except:
                        properties.append((key,row[key]))
                
                properties = {key: value for key, value in properties}
                
                data_toAssimilate[row[data_idName]]=properties  
                continue

            # Open boundary geoJSON file
            with open(geo_path, 'r') as boundaryFile:
                
                boundaries = json.load(boundaryFile)
                # For row in CSV insert columns as properties in geoJSON
                for boundary in boundaries["features"]:
                    properties = boundary["properties"]
                    boundary["properties"]=data_toAssimilate[properties[geo_idName]]

                data_assimilated = boundaries
                
    
    #If input is dictionary / json
    elif data_type == "dict":
        
        data_toAssimilate=data_path
        # Open boundary geoJSON file
        with open(geo_path, 'r') as boundaryFile:
            boundaries = json.load(boundaryFile)

            # For row in CSV insert columns as properties in geoJSON
            for boundary in boundaries["features"]:
                properties = boundary["properties"]
                boundary["properties"]=data_toAssimilate[properties[geo_idName]]

            data_assimilated = boundaries
    
    # Save
    with open(out_path, 'w') as out:
       json.dump(data_assimilated, out)
       
    print("Message (B2): Successfully assimilated: ", out_path)