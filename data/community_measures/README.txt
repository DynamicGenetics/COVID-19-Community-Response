Description:
A utility which gets the live source data for covid community locations and converts it into a validated geoJSON format. 

Instructions:
ACTIVE VERSION (v3+) - 3 Python (live)
WIP. Simply run the index file and a python server to scrape the police coders google sheet, using google docs / sheets API

Methods:
Scrape data from google sheet (scrape), 
Remove duplicates (removeDuplicates), 
Geolocate groups to Wales and remove non-welsh groups (geoLocate)

Definition:
def googleScrape(URL, SpreadsheetID, SpreadsheetRange)

Arguments:
URL = url of spreadsheet (i.e., http:/google.com/sheets/)
SpreadsheetID = ID of spreadsheet (i.e., .../5874587230fds)
SpreadsheetRange = range of data in spreadsheet to obtain (e.g., sheet name or rows)


Legacy versions

(Deprecated)
1 Javascript:
Simply run the index html file and the javascript will automatically call the covid mutual aid web page

(Deprecated)
2 Python (local):
Simply run the python file adn it will convert CSV to geoJSON for locally stored data.
