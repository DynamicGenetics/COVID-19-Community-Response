from recompiler import convertGroups
from scraper import googleScrape
from QC.QC import QCFilter

#Scrape data from google sheet
googleScrape()

#Convert csv to geoJSON using method from recompiler.py
convertGroups()