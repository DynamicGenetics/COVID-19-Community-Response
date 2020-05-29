"""Module containing functions required for attaining and cleaning data on COVID cases in each
Local Authority from the Public Health Wales dashboard.
"""

import requests
import os
import pandas as pd
from .get_data_url import get_data_link


def run_phw_scraper(raw_folder, cleaned_folder):
    """Get latest data from PHW.

    This function will get the latest data, write it to the raw folder as a .xlsx.
    It will then clean it it, and write the cleaned data to the clean folder.

    Parameters
    ----------
    raw_folder : str
        File path to write the raw scraped data to.
    cleaned_folder : str
        File path to write the cleaned data to.
    """

    name = "phwCovidStatement"
    raw = os.path.join(raw_folder, name + ".xlsx")
    cleaned = cleaned_folder = os.path.join(cleaned_folder, name + ".csv")

    get_phw_data(raw)
    covid = clean_data(raw, cleaned)

    print(
        "Message (phwScraper): Scraped covid data (latest data found: {})".format(covid)
    )


def get_phw_data(output_path):
    """Downloads PHW dashboard data Excel file, saves as xlsx to given output path.

    Runs the function `get_data_link`.

    Parameters
    ----------
    output_path : str
        File path to raw data output location
    """

    # Download data download for phw covid cases statement
    try:
        url = get_data_link()
    except Exception as e:
        url = "http://www2.nphs.wales.nhs.uk:8080/CommunitySurveillanceDocs.nsf/3dc04669c9e1eaa880257062003b246b/77fdb9a33544aee88025855100300cab/$FILE/Rapid%20COVID-19%20surveillance%20data.xlsx"
        raise e

    r = requests.get(url, allow_redirects=True)

    # Save in native xlsx format
    output = open(output_path, "wb")
    output.write(r.content)
    output.close()


def clean_data(input_path, output_path):
    """Given an input path, will read the raw data from there, select the sheet with the
    COVID cases data, get the most recent data and match it to the correct local authority codes.

    Parameters
    ----------
    input_path : str
        File path to read the raw data from
    output_path : str
        File path to write the cleaned data to

    Returns
    -------
    str, list
        String of most recent date data was collected from, and a list of the column names written
        to .csv.
    """
    # Read sheet contianing COVID case data from phw statement
    df = pd.read_excel(input_path, sheet_name="Tests by specimen date")

    # Get most recent date in data
    df["Specimen date"] = pd.to_datetime(df["Specimen date"])
    recent_date = df["Specimen date"].max()

    # Filter data by the latest date
    cleaned = df[df["Specimen date"] == recent_date]

    # Clean data by removing unused columns
    cleaned = cleaned.drop(
        [
            "Specimen date",
            "Cases (new)",
            "Cumulative cases",
            "Testing episodes (new)",
            "Cumulative testing episodes",
        ],
        axis=1,
    )

    # Remove data for outside of wales and unknown areas
    cleaned = cleaned[cleaned["Local Authority"] != "Outside Wales"]
    cleaned = cleaned[cleaned["Local Authority"] != "Unknown"]

    # Look up and append area IDs since these are used as the area identifiers in the geojson and layer processes later
    cleaned["areaID"] = cleaned.apply(
        lambda row: area_code(row["Local Authority"]), axis=1
    )

    # Rename columns to make consistent with other data files used for mapping
    cleaned = cleaned.rename(
        columns={
            "Local Authority": "la_name",
            "Cumulative incidence per 100,000 population": "covidIncidence_100k",
            "areaID": "areaID",
        }
    )

    # Save cleaned data frame as csv in cleaned data folder
    cleaned.to_csv(output_path, index=None, header=True)

    # Return date and list column headers to print in console for information on data collected
    return (recent_date, list(cleaned.columns))


def area_code(laName):
    """For Local Authority name given, returns the corresponding code."""

    # If header, creare new header for area ID col
    if laName == "Local Authority":

        return "areaID"

    # For data rows in the csv, use la area name to look up la area code
    else:

        # LA : LA code dictionary
        laCode = {
            "Blaenau Gwent": "W06000019",
            "Bridgend": "W06000013",
            "Caerphilly": "W06000018",
            "Cardiff": "W06000015",
            "Carmarthenshire": "W06000010",
            "Ceredigion": "W06000008",
            "Conwy": "W06000003",
            "Denbighshire": "W06000004",
            "Flintshire": "W06000005",
            "Gwynedd": "W06000002",
            "Isle of Anglesey": "W06000001",
            "Merthyr Tydfil": "W06000024",
            "Monmouthshire": "W06000021",
            "Neath Port Talbot": "W06000012",
            "Newport": "W06000022",
            "Pembrokeshire": "W06000009",
            "Powys": "W06000023",
            "Rhondda Cynon Taf": "W06000016",
            "Swansea": "W06000011",
            "Torfaen": "W06000020",
            "Vale of Glamorgan": "W06000014",
            "Wrexham": "W06000006",
        }

        # For la area name, return la area code
        return laCode[laName]
