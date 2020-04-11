from recompiler import convertCases
from scraper import webScrape

#Scrape from URL to FILENAME
webScrape('https://covid19-phwstatement.nhs.wales/', 'cases.csv')

#Convert output FILENAME to FILENAME.geojson
convertCases('cases.csv')