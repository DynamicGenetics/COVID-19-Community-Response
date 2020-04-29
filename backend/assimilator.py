import csv
import json


def assimilate(data_type, data_path, data_idName, geo_path, geo_idName, out_path):
    data_toAssimilate = {}

    # If input is csv
    if data_type == "csv":

        # Open the CSV as dictionary
        with open(data_path, newline="") as f:
            reader = csv.DictReader(f)

            # Make dictionary of all columns in csv
            for row in reader:
                properties = []

                for key in row:

                    try:
                        properties.append((key, float(row[key].replace(",", "",))))
                    except:
                        properties.append((key, row[key]))

                properties = {key: value for key, value in properties}

                data_toAssimilate[row[data_idName]] = properties
                continue

            # Open boundary geoJSON file
            with open(geo_path, "r") as boundaryFile:

                boundaries = json.load(boundaryFile)

                # For row in CSV insert columns as properties in geoJSON
                for boundary in boundaries["features"]:
                    properties = boundary["properties"]
                    
                    boundary["properties"] = data_toAssimilate[properties[geo_idName]]
                    
                data_assimilated = boundaries

    # If input is dictionary / json
    elif data_type == "dict":

        data_toAssimilate = data_path
        # Open boundary geoJSON file
        with open(geo_path, "r") as boundaryFile:
            boundaries = json.load(boundaryFile)

            # For row in CSV insert columns as properties in geoJSON
            for boundary in boundaries["features"]:
                properties = boundary["properties"]
                boundary["properties"] = data_toAssimilate[properties[geo_idName]]

            data_assimilated = boundaries

    # If input is points
    elif data_type == "points":
        point_features = []

        #Read in csv as list of dictionaries so each row is a dictionary with {headers : values}
        with open(data_path, newline="", encoding="utf8") as f:
            reader = csv.DictReader(f)
            
            try:
                for row in reader:
                    properties = []

                    for key in row:
                        try:
                            properties.append((key, float(row[key].replace(",", "",))))
                        except:
                            properties.append((key, row[key]))
                    
                    #For each point (row in csv), detect and extract all headers (dictionary keys), store values, and add to list of dictionaries
                    properties = {key: value for key, value in properties}

                    #Form geojson format for points, dump properties as dictionaries into properties
                    point_features.append({
                        "type": "Feature",
                        "geometry": {"type": "Point", "coordinates": [float(row['Lng']), float(row['Lat'])]},
                        "properties": properties,
                    })
            except:
                print("WARNING (Assimilator): Unable to assimilate row: ", row)
            
            print("Message (Assimilator): Found {} points for {} ".format(len(point_features),data_path))
            
            #Output list of features (with properties) in geojson format; convert to list for json serialisation by using sorted()
            data_assimilated = {"type": "FeatureCollection", "features": point_features}

    # Save
    with open(out_path, "w") as out:
        json.dump(data_assimilated, out)

    print("Message (Assimilator): Successfully assimilated: ", out_path)
