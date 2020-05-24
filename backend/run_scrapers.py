"""
Intended purpose of this script:
1. Get updated data using police_coders_scrape () & phwScraper()
2. Save scraping data archived by date (csv)
3. Overwrite most recent data (csv)
4. Produce groupCount layer as a count of groups per area

police_coders_scrape () function:
Uses google sheets API to get Police Coders group list, saves as CSV

phw_scrape() function:
Downloads PHW dashboard data Excel file, saves as xlsx

groupCount() function:
Count the number of groups per area to produce the groupCount layer
"""

from scrapers.police_coders_groups.police_scraper import police_coders_scrape
from scrapers.police_coders_groups.localise import (
    get_welsh_boundary,
    filter_welsh_groups,
    write_data_to_CSV,
)
from scrapers.police_coders_groups.group_count import (
    count_groups,
    get_boundaries_LA,
    get_boundaries_LSOA,
    locate_group,
)
from scrapers.phw_covid_statement.phw_scraper import phw_scrape, area_code, clean_data


# run Police Coders community group scraper
if __name__ == "__main__":

    # Define file output paths
    fn_groups_raw = "backend/data/live/raw/groups_raw.csv"
    fn_groups_cleaned = "backend/data/live/cleaned/groups.csv"
    root_path = "backend/scrapers/police_coders_groups/"

    # Get latest community group data
    groups = police_coders_scrape(fn_groups_raw, root_path)
    print("Message (police_coders_scrape): Scraped group count: ", groups)

    # Get welsh border as polygon Shape object
    welsh_border_polygon = get_welsh_boundary(
        "backend/data/static/geoboundaries/boundaries_Wales.geojson"
    )

    # Search if group coordinates are located within welsh border Shape object
    welsh_groups = filter_welsh_groups(fn_groups_raw, welsh_border_polygon)

    # Write list of welsh groups to csv
    write_data_to_CSV(welsh_groups[0], welsh_groups[1], fn_groups_cleaned)

    # Count the number of groups per area to produce the groupCount layer

    # Get boundary shapes and names for la and lsoa levels
    boundary_info_LA = get_boundaries_LA(
        "backend/data/static/geoboundaries/boundaries_LA.geojson"
    )
    boundary_info_LSOA = get_boundaries_LSOA(
        "backend/data/static/geoboundaries/boundaries_LSOA.geojson"
    )

    # Make seperate counts of groups per la and lsoa
    count_LA = count_groups(
        "backend/data/live/cleaned/groups.csv", boundary_info_LA, "lad18cd"
    )
    count_LSOA = count_groups(
        "backend/data/live/cleaned/groups.csv", boundary_info_LSOA, "LSOA11CD"
    )

    print(
        "Message (groupCount): Performed count of groups per area, {} groups localised to LAs and {} to LSOAs".format(
            count_LA["groupCount"].sum(), count_LSOA["groupCount"].sum()
        )
    )

    # Save counts of groups by areas to seperate csvs
    count_LA.to_csv("backend/data/live/cleaned/groupCount_LA.csv", index=False)
    count_LSOA.to_csv("backend/data/live/cleaned/groupCount_LSOA.csv", index=False)


# run PHW Covid Case scraper
if __name__ == "__main__":

    # Get latest covid case data from PHW
    phw_scrape("backend/data/live/raw/phwCovidStatement.xlsx")

    # Clean into format the data pipeline is expecting
    covid = clean_data(
        "backend/data/live/raw/phwCovidStatement.xlsx",
        "backend/data/live/cleaned/phwCovidStatement.csv",
    )
    print(
        "Message (phwScraper): Scraped covid data (latest data found: {})".format(covid)
    )
