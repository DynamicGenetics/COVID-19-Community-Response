import csv  
import json  

data_toAssimilate={}

def assimilate(filename_input, filename_boundaries, lsoaIDColName, filename_output):
    print("ASSIMILATING: ", filename_input)
    
    # Open the CSV as dictionary  
    with open(filename_input, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        
        # Make dictionary of all columns in csv
        for row in reader:
            properties=[]
            
            for key in row:
                properties.append({key:row[key]})
                continue
                
            data_toAssimilate[row[lsoaIDColName]]=properties  
            continue
            
        # Open boundary geoJSON file
        with open(filename_boundaries, 'r') as boundaryFile:
            boundaries = json.load(boundaryFile)
                        
            # For row in CSV insert columns as properties in geoJSON
            for boundary in boundaries["features"]:
                properties = boundary["properties"]
                boundary["properties"]=data_toAssimilate[properties["lad18cd"]]
                
            data_assimilated = boundaries

    # Save
    with open(filename_output, 'w') as out:
       json.dump(data_assimilated, out)
    print("ASSIMILATED TO: ", filename_output)