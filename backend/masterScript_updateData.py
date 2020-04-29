from scrapers.police_coders_groups.scraper import googleScrape
from scrapers.police_coders_groups.countGroups import countGroups
from scrapers.police_coders_groups.localise import *

def obtain_new_data():

    groups = googleScrape("backend/data/raw/groups")
    print("Message (googleScrape): Scraped group count: ", groups)
    
    #Sums of groups per area disabled until fixed
    #count = countGroups('backend/data/transformed/groups.csv')
    #print(count)

    iterateGroups(
        'backend/data/raw/groups_raw.csv',
        'backend/data/cleaned/groups.csv', 
        'backend/data/geoboundaries/boundaries_Wales.geojson'
    )

obtain_new_data()