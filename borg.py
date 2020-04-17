# Import data sources dict
from dataSources import dataSources, boundaryFiles, filenames

# Import slave functions to call in these master functions (debug name = B1)
from assimilator import assimilate
from data.community_measures.recompiler import groupProcessing
from data.community_measures.scraper import googleScrape
from data.community_measures.QC.QC import QCFilter
from data.community_measures.QC.detectDuplicate import detectDuplicate
from data.community_measures.saveOutput import saveOutput

count_data = 0
count_dataEnabled = 0
count_dataSuccess = 0

# Iterate over data sources in dataSources dictionary 
for data in dataSources:

    # Proceed with data unless marked as 'disabled'
    if data["enabled"] == True:

        try: 
            
            # If data marked as 'csv' directly recompile as geojson 
            if data["type"] == 'csv':

                    # Assimilate() csv as properties into geojson boundary file
                    geo = boundaryFiles[data['res']]
                    assimilate(data['type'], data['path'], data['ID_name'], geo['path'], geo['ID_name'], 'data/{}.geojson'.format(data['name']))

             # If data marked as 'scrape', scrape data first then recompile as geojson
            elif data["type"] == 'scrape':

                    # Scrape data from google sheet, remove duplicates, geolocate to Wales and convert csv to geoJSON
                    googleScrape('https://www.googleapis.com/auth/spreadsheets.readonly', '1iqOvNjRlHIpoRzd61BcBLVkSxGvbta6vrzH2Jgc50aY', 'Support groups v2', filenames['credentials'], filenames['csv'])
                    groupsData = groupProcessing(filenames)
                    saveOutput(groupsData[0], groupsData[1], groupsData[2], groupsData[3], filenames)
                    #for row in groupsData[4]: print(row)
            
            count_dataSuccess += 1
            print('Message (Borg): Assimilating {} (type={}) '.format(data['name'],data['type']))

        except:
            print('ERROR (Borg): Could not assimilate: ', data['name'])
        
        count_dataEnabled +=1
        
    # Skip data marked as 'disabled'
    else:
        print("Warning (Borg): Skipping disabled data: ", data['name'])
    count_data +=1

print("BORG HAS ASSIMILATED {} / {} COMPATIABLE DATA SOURCES ({} enabled)".format(count_dataSuccess, count_data, count_dataEnabled))