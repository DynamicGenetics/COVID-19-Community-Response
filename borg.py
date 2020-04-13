from data.recompilers.borg import assimilate
from data.live.groups.recompiler import convertGroups
from data.live.groups.scraper import googleScrape
from data.live.groups.QC.QC import QCFilter

# Produce demographics data
assimilate("csv", "data/static/demographics/demographics.csv", "data/boundaries_LSOAs.geoJSON", "id_area", "data/demographics.geojson")

# Produce cases data
assimilate("csv", "data/live/cases-manual/cases.csv", "data/boundaries_LSOAs.geoJSON", "id_area", "data/cases.geojson")

# Scrape data from google sheet, remove duplicates, geolocate to Wales and convert csv to geoJSON
googleScrape('https://www.googleapis.com/auth/spreadsheets.readonly', '117ukLjXiz8EfMjP-q9Aiu5XepQ39XK1W4DTMsE87llw', 'Support groups')
groupsData = convertGroups("data/boundaries_wales.geoJSON", "data/boundaries_LSOAs.geoJSON", "data/live/groups/groups.csv", "data/static/demographics/demographics.csv", "data/groups.geojson", "data/groupCount.geojson", "data/live/groups/URLs.json", "data/live/groups/QC/groupsForReview.csv")
#WIP: assimilate("dict", groupsData, "data/boundaries_LSOAs.geoJSON", None, "data/cases.geojson")

# Scrape data from COVID cases dataset
#WIP: