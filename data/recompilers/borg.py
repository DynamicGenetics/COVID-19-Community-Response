import csv  
import json  

def assimilate(dataType, input_data, filename_boundaries, lsoaIDColName, filename_output):
    data_toAssimilate={}
    print("ASSIMILATING: ", input_data)
    
    #If input is csv
    if dataType == "csv":

        # Open the CSV as dictionary  
        with open(input_data, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            # Make dictionary of all columns in csv
            for row in reader:
                properties=[]

                for key in row:
                    properties.append((key,row[key]))
                
                properties = {key: value for key, value in properties}

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
                
    
    #If input is dictionary / json
    elif dataType == "dict":
        
        data_toAssimilate=input_data
        
        # Open boundary geoJSON file
        with open(filename_boundaries, 'r') as boundaryFile:
            boundaries = json.load(boundaryFile)

            # For row in CSV insert columns as properties in geoJSON
            for boundary in boundaries["features"]:
                properties = boundary["properties"]
                boundary["properties"]=data_toAssimilate[properties["lad18cd"]]

            data_assimilated = boundaries
    
    # Save
    print("ASSIMILATED TO: ", filename_output)
    with open(filename_output, 'w') as out:
       json.dump(data_assimilated, out)