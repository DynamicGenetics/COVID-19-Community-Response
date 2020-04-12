from data.recompilers.borg import assimilate
from data.live.groups.recompiler import convertGroups
from data.live.groups.scraper import googleScrape

# Produce demographics data
assimilate("../static/demographics/demographics.csv", "../boundaries_LSOAs.geoJSON", "id_area", "../demographics.geojson")

# Produce cases data
assimilate("../live/cases-manual/cases.csv", "../boundaries_LSOAs.geoJSON", "id_area", "../cases.geojson")

# Scrape data from google sheet, remove duplicates, geolocate to Wales and convert csv to geoJSON
googleScrape()
convertGroups()

# Scrape data from COVID cases dataset