from data.scrapers.police_coders_groups.scraper import googleScrape
from data.scrapers.police_coders_groups.countGroups import countGroups
from localise import *

def obtain_new_data():

    groups = googleScrape("data/scrapers/police_coders_groups/archive/groups")
    print("Message (googleScrape): Scraped group count: ", groups)
    
    #Sums of groups per area
    #count = countGroups()
    #print(count)

    iterateGroups('data/scrapers/police_coders_groups/groups_raw.csv','data/scrapers/police_coders_groups/groups.csv', 'data/geography/boundaries_Wales.geojson')

obtain_new_data()