"""
Intended purpose of this script:
1. Get updated data using police_coders_scrape () & phwScraper()
2. Save scraping data archived by date (csv)
3. Overwrite most recent data (csv)
4. Produce groupCount layer as a count of groups per area
"""

from datasets import LIVE_DATA_FOLDER, LIVE_RAW_DATA_FOLDER, GEO_DATA_FOLDER

from scrapers.police_coders_groups.run_scraper import run_police_coders_scraper
from scrapers.phw_covid_statement.phw_scraper import run_phw_scraper

if __name__ == "__main__":
    # Get latest covid case data from PHW
    run_phw_scraper(LIVE_RAW_DATA_FOLDER, LIVE_DATA_FOLDER)
    # run  Coders community group scra
    run_police_coders_scraper(LIVE_RAW_DATA_FOLDER, LIVE_DATA_FOLDER, GEO_DATA_FOLDER)
