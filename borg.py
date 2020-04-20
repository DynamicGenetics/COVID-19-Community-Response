# Import data sources dict
from dataSources import *

# Import slave functions to call in these master functions (debug name = B1)
from assimilator import assimilate
from data.community_measures.recompiler import groupProcessing
from data.community_measures.scraper import googleScrape
from data.community_measures.QC.QC import QCFilter
from data.community_measures.QC.detectDuplicate import detectDuplicate
from data.community_measures.saveOutput import saveOutput
from visualisation.generateLayer import generateLayer

count_data = 0
count_dataEnabled = 0
count_dataSuccess = 0
skipped_data = []

# Setting this to true will run the scraping operations when this file is ran
runScraping = False

# Iterate over data sources in dataSources dictionary
for data in DATASOURCES:

    # Proceed with data unless marked as 'disabled'
    if data["enabled"] == True:

        try:

            # If data marked as 'csv' directly recompile as geojson
            if data["type"] == "csv":

                # Assimilate() csv as properties into geojson boundary file
                geo = BOUNDARYFILES[data["res"]]
                assimilate(
                    data["type"],
                    data["path"],
                    data["ID_name"],
                    geo["path"],
                    geo["ID_name"],
                    "data/{}.geojson".format(data["name"]),
                )

            # If data marked as 'scrape', scrape data first then recompile as geojson
            elif data["type"] == "scrape":
                # Scrape data from google sheet, remove duplicates, geolocate to Wales and convert csv to geoJSON
                if runScraping:
                    googleScrape(
                        "https://www.googleapis.com/auth/spreadsheets.readonly",
                        "1iqOvNjRlHIpoRzd61BcBLVkSxGvbta6vrzH2Jgc50aY",
                        "Support groups v2",
                        FILENAMES["credentials"],
                        FILENAMES["csv"],
                    )
                groupsData = groupProcessing(FILENAMES)
                saveOutput(
                    groupsData[0],
                    groupsData[1],
                    groupsData[2],
                    groupsData[3],
                    FILENAMES,
                )
                # for row in groupsData[4]: print(row)

            elif data["type"] == "geojson":
                continue

            count_dataSuccess += 1
            print(
                "Message (Borg): Assimilating {} (type={}) ".format(
                    data["name"], data["type"]
                )
            )

        except:
            print("ERROR (Borg): Could not assimilate: ", data["name"])

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
