# Import data sources information
from data.dataSources import *

# Import  functions to call
from assimilator import assimilate
from generateLayer import generateLayer

# Initialise counts to count successful and unsuccessful operations
count_data = 0
count_dataEnabled = 0
count_dataSuccess = 0

# Initialise list of data sources marked as disabled
skipped_data = []


'''
Intended purpose of this script: 
1. Feed data source metadata into assimilate()
2. Generate geojson files from raw files 

Assimilate () function:
If input is csv then rows are inserted as properties into geojson boundary file
else If input is geojson then point features are formatted into geojson
'''

# Use source information to access filenames and metadata to produce geojsons 
for data in DATASOURCES:

    # Proceed with data unless marked as 'disabled'
    if data["enabled"] == True:

        # If data marked as 'geojson' then skip, or else recompile as geojson
        if data["type"] == "geojson":
            continue
            
        # Run Assimilate() for each data source
        else:
            geo = BOUNDARYFILES[data["res"]]
            assimilate(
                data["type"],
                data["path"],
                data["ID_name"],
                geo["path"],
                geo["ID_name"],
                "dashboard/data/{}.geojson".format(data["name"]),
            )

        # Increment counts for enabled data sources and successful assimilations
        count_dataEnabled += 1
        count_dataSuccess += 1

        print(
            "Message (createMapLayers): Assimilating {} (type={}) ".format(
                data["name"], data["type"]
            )
        )

    # Skip data sources marked as 'disabled'
    else:
        skipped_data.append(data["name"])
    
    # Increment count for total number of data sources 
    count_data += 1


# Generate map layers for each data layer
layers = generateLayer(DATASOURCES, "dashboard/layers.js")
print(layers)

print(
    "ASSIMILATED {} / {} COMPATIABLE DATA SOURCES ({} enabled, disabled: {})".format(
        count_dataSuccess, count_data, count_dataEnabled, skipped_data
    )
)