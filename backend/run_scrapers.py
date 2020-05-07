"""
Intended purpose of this script:
1. Get updated data using googleScrape () & phwScraper()
2. Save scraping data archived by date (csv)
3. Overwrite most recent data (csv)

police_coders_scrape () function:
Uses google sheets API to get Police Coders group list, saves as CSV

phw_scrape() function:
Downloads PHW dashboard data Excel file, saves as xlsx
"""

from scrapers.police_coders_groups.police_scraper import police_coders_scrape
from scrapers.police_coders_groups.count_groups import count_groups
from scrapers.police_coders_groups.localise import (
    get_welsh_boundary,
    filter_welsh_groups,
    write_data_to_CSV,
)
from scrapers.phw_covid_statement.phw_scraper import phw_scrape, area_code, clean_data


# run Police Coders community group scraper
if __name__ == "__main__":

    # Define file output paths
    fn_groups_raw = "backend/data/live/raw/groups_raw.csv"
    fn_groups_cleaned = "backend/live/data/cleaned/groups.csv"

    # Get latest community group data
    groups = police_coders_scrape(fn_groups_raw)
    print("Message (googleScrape): Scraped group count: ", groups)

    # TEMP: Data layer disabled: The count of community groups per area
    # count = count_groups('backend/data/transformed/groups.csv')
    # print(count)

    # Get welsh border as polygon Shape object
    welsh_border_polygon = get_welsh_boundary(
        "backend/data/static/geoboundaries/boundaries_Wales.geojson"
    )

    # Search if group coordinates are located within welsh border Shape object
    welsh_groups = filter_welsh_groups(fn_groups_raw, welsh_border_polygon)

    # Write list of welsh groups to csv
    write_data_to_CSV(welsh_groups[0], welsh_groups[1], fn_groups_cleaned)


# run PHW Covid Case scraper
if __name__ == "__main__":

    # Get latest covid case data from PHW
    phw_scrape("backend/data/live/raw/phwCovidStatement.xlsx")

    covid = clean_data(
        "backend/data/live/raw/phwCovidStatement.xlsx",
        "backend/data/live/cleaned/phwCovidStatement.csv",
    )
    print(
        "Message (phwScraper): Scraped covid data (latest data found: {})".format(covid)
    )
