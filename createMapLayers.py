# Import data sources dict
from dataSources import *

# Import slave functions to call in these master functions (debug name = B1)
from assimilator import assimilate
from visualisation.generateLayer import generateLayer

count_data = 0
count_dataEnabled = 0
count_dataSuccess = 0
skipped_data = []

# Iterate over data sources in dataSources dictionary
for data in DATASOURCES:

    # Proceed with data unless marked as 'disabled'
    if data["enabled"] == True:

        # If data marked as 'geojson' then skip, or else recompile as geojson
        if data["type"] == "geojson":
            continue

        # Assimilate() csv properties/points as properties into geojson boundary file
        else:
            geo = BOUNDARYFILES[data["res"]]
            assimilate(
                data["type"],
                data["path"],
                data["ID_name"],
                geo["path"],
                geo["ID_name"],
                "data/{}.geojson".format(data["name"]),
            )

        count_dataSuccess += 1
        print(
            "Message (Borg): Assimilating {} (type={}) ".format(
                data["name"], data["type"]
            )
        )

        #except:
        #    print("ERROR (Borg): Could not assimilate: ", data["name"])

        count_dataEnabled += 1

    # Skip data marked as 'disabled'
    else:
        # print("Warning (Borg): Skipping disabled data: ", data['name'])
        skipped_data.append(data["name"])
    count_data += 1

# Dynamically generate layers
layers = generateLayer(DATASOURCES, "visualisation/borgLayers.js")

print(layers)

print(
    "BORG HAS ASSIMILATED {} / {} COMPATIABLE DATA SOURCES ({} enabled, disabled: {})".format(
        count_dataSuccess, count_data, count_dataEnabled, skipped_data
    )
)