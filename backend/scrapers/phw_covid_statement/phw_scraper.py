import requests
import pandas as pd
from datetime import datetime


def phw_scrape(output_path):

    # Download data download for phw covid cases statement
    url = "http://www2.nphs.wales.nhs.uk:8080/CommunitySurveillanceDocs.nsf/61c1e930f9121fd080256f2a004937ed/77fdb9a33544aee88025855100300cab/$FILE/Rapid%20COVID-19%20surveillance%20data.xlsx"
    r = requests.get(url, allow_redirects=True)

    # Save in native xlsx format
    output = open(output_path, "wb")
    output.write(r.content)
    output.close()


def clean_data(input_path, output_path):

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

    # Return data and list column headers to print in console for information on data collected
    return (recent_date, list(cleaned.columns))


def area_code(laName):

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
