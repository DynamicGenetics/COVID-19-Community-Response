from scrapers.police_coders_groups.scraper import googleScrape
from scrapers.police_coders_groups.countGroups import countGroups
from scrapers.police_coders_groups.localise import *
from scrapers.phw_covid_statement.phwScraper import *

'''
Intended purpose of this script: 
1. Get updated data using googleScrape () & phwScraper()
2. Save scraping data archived by date (csv)
3. Overwrite most recent data (csv)

googleScrape () function:
Uses google sheets API to get Police Coders group list, saves as CSV

phwScraper() function:
Downloads PHW dashboard data Excel file, saves as xlsx
'''

def obtain_new_data():

    # Get new group data

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

    # Get new covid cases data
    
    phwScraper('backend/data/raw/phwCovidStatement.xlsx')
    print("Message (phwScraper): Successfully scraped covid data")
    
    covid = cleanData('backend/data/raw/phwCovidStatement.xlsx','backend/data/cleaned/phwCovidStatement.csv')
    print("Message (phwScraper): Scraped covid data (latest data found: {})".format(covid))
    
obtain_new_data()