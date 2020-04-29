from scrapers.police_coders_groups.scraper import googleScrape
from scrapers.police_coders_groups.countGroups import countGroups
from scrapers.police_coders_groups.localise import *

'''
Intended purpose of this script: 
1. Get updated data using googleScrape ()
2. Save scraping data archived by date (csv)
3. Overwrite most recent data (csv)

googleScrape () function:
Uses google sheets API to get Police Coders group list, saves as CSV
'''

def obtain_new_data():

    groups = googleScrape("backend/data/raw/groups")
    print("Message (googleScrape): Scraped group count: ", groups)
    
    #Data layer disabled: The count of community groups per area
    #count = countGroups('backend/data/transformed/groups.csv')
    #print(count)

    iterateGroups(
        'backend/data/raw/groups_raw.csv',
        'backend/data/cleaned/groups.csv', 
        'backend/data/geoboundaries/boundaries_Wales.geojson'
    )

obtain_new_data()