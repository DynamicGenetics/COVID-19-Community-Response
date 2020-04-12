from data.recompilers.borg import assimilate, deconstruct
from data.recompilers.borg import *

#Scrape from URL to FILENAME
scrape('https://covid19-phwstatement.nhs.wales/', 'cases.csv')

#Convert output FILENAME to FILENAME.geojson
convert('cases.csv')