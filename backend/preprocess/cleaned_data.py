"""Module that generates the cleaned datasets for each variable from raw"""

# Import packages
import pandas as pd
import geopandas as gpd

# Import functions from package in backend/data/static/preprocess
from preprocess import clean_data

# Import all the raw data constants
from data.static import raw_data as r

from dataclasses import dataclass


@dataclass
class CleaningReqs:
    """Class for mapping the changes needed to clean each dataset"""

    data: pd.DataFrame
    res: str  # Resolution at 'LSOA' or 'LA'
    key_col: str  # Name of the column that has a unique key
    key_is_code: bool  # Is the key column a LA or LSOA code?
    csv_name: str  # Name for the output CSV
    keep_cols: list = []  # List of columns specifically wanted to keep
    bracketed_data_cols: list = None  # List of columns where data is in the format (DATA (PERCENT))
    rename_dict: dict = None  # Dictionary of columns that need renaming CleaningReqs('old_name' : 'new_name' }


LSOA_WELSH_DICT = CleaningReqs(
    data=r.RAW_WELSH_LSOA,
    res="LSOA",
    key_col="Unnamed: 2",
    key_is_code=True,
    csv_name="welsh_speakers_percent",
    rename_dict={"Percentage able to speak Welsh ": "welsh_speakers_percent"},
)

LA_WELSH_DICT = CleaningReqs(
    data=r.RAW_WELSH_LA,
    res="LA",
    key_col="Unnamed: 1",
    key_is_code=False,
    csv_name="welsh_speakers_percent",
    rename_dict={
        "Daily ": "welsh_daily_percent",
        "Weekly ": "welsh_weekly_percent",
        "Less Often ": "welsh_lessoften_percent",
    },
)

LSOA_POPULATION_DICT = CleaningReqs(
    data=r.RAW_POPDENSITY_LSOA,
    res="LSOA",
    key_col="Area Codes",
    key_is_code=True,
    csv_name="population_count",
    rename_dict={"All Ages": "population_count"},
)

LA_POPULATION_DICT = CleaningReqs(
    data=r.RAW_POPULATION_LA,
    res="LA",
    key_col="Unnamed: 3",
    key_is_code=False,
    csv_name="population_count",
    rename_dict={"All ages .1": "population_count"},
)

LSOA_OVER_65_DICT = CleaningReqs(
    data=r.RAW_OVER_65_LSOA,
    res="LSOA",
    key_col="Area Codes",
    key_is_code=True,
    csv_name="over_65_count",
)

LA_OVER_65_DICT = CleaningReqs(
    data=r.RAW_OVER_65_LA,
    res="LA",
    key_col="Unnamed: 3",
    key_is_code=False,
    csv_name="over_65_count",
    rename_dict={"Unnamed: 14": "over_65_count"},
)

LSOA_IMD_DICT = CleaningReqs(
    data=r.RAW_IMD_LSOA,
    res="LSOA",
    key_col="lsoa11cd",
    key_is_code=True,
    csv_name="wimd_2019",
    keep_cols=["LSOA11CD", "wimd_2019"],
)

LA_IMD_DICT = CleaningReqs(
    data=r.RAW_IMD_LA,
    res="LA",
    key_col="Unnamed: 0",
    key_is_code=False,
    csv_name="wimd_2019",
)

LSOA_POPDENSITY_DICT = CleaningReqs(
    data=r.RAW_POPDENSITY_LSOA,
    res="LSOA",
    key_col="Code",
    key_is_code=True,
    rename_dict={"People per Sq Km": "pop_density_persqkm"},
    keep_cols=["LSOA11CD", "pop_density_persqkm"],
    csv_name="pop_density_persqkm",
)

LA_POPDENSITY_DICT = CleaningReqs(
    data=r.RAW_POPDENSITY_LA,
    res="LA",
    key_col="Unnamed: 1",
    key_is_code=False,
    rename_dict={"Mid-year 2018 ": "pop_density_persqkm"},
    csv_name="pop_density_persqkm",
)

LA_VULNERABLE_DICT = CleaningReqs(
    data=r.RAW_VULNERABLE_LA,
    res="LA",
    key_col="index",
    key_is_code=False,
    rename_dict={38: "vulnerable"},
    bracketed_data_cols=["vulnerable"],
    csv_name="vulnerable_count_percent",
)

LA_COHESION_DICT = CleaningReqs(
    data=r.RAW_COMM_COHESION_LA,
    res="LA",
    key_col="index",
    key_is_code=False,
    rename_dict={20: "belong_strongagree", 21: "belong_agree"},
    bracketed_data_cols=["belong_strongagree", "belong_agree"],
    csv_name="comm_cohesion_count_percent",
)

LA_INTERNET_ACCESS_DICT = CleaningReqs(
    data=r.RAW_INTERNET_ACCESS_LA,
    res="LA",
    key_col="Unnamed: 0",
    key_is_code=False,
    rename_dict={"Yes (%)": "has_internet_percent"},
    csv_name="has_internet_percent",
)

LA_INTERNET_USE_DICT = CleaningReqs(
    data=r.RAW_INTERNET_USE_LA,
    res="LA",
    key_col="Unnamed: 0",
    key_is_code=False,
    rename_dict={
        "Several times a day (%)": "use_several_daily_percent",
        "Daily (%) ": "use_daily_percent",
    },
    csv_name="use_internet_percent",
)

LA_ETHNICITY_DICT = CleaningReqs(
    data=r.RAW_ETHNICITY_LA,
    res="LA",
    key_col="Unnamed: 1",
    key_is_code=False,
    csv_name="ethnicities_percent",
)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Apply functions to each dataset, and create new constant
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
WELSH_LSOA = clean_data(LSOA_WELSH_DICT)
WELSH_LA = clean_data(LA_WELSH_DICT)
POPULATION_LSOA = clean_data(LSOA_POPDENSITY_DICT)
POPULATION_LA = clean_data(LA_POPULATION_DICT)
OVER_65_LSOA = clean_data(LSOA_OVER_65_DICT)
OVER_65_LA = clean_data(LA_OVER_65_DICT)
IMD_LSOA = clean_data(LSOA_IMD_DICT)
IMD_LA = clean_data(LA_IMD_DICT)
POPDENSITY_LSOA = clean_data(LSOA_POPDENSITY_DICT)
POPDENSITY_LA = clean_data(LA_POPDENSITY_DICT)
VULNERABLE_LA = clean_data(LA_VULNERABLE_DICT)
COMM_COHESION_LA = clean_data(LA_COHESION_DICT)
INTERNET_ACCESS_LA = clean_data(LA_INTERNET_ACCESS_DICT)
INTERNET_USE_LA = clean_data(LA_INTERNET_USE_DICT)
ETHNICITY_LA = clean_data(LA_ETHNICITY_DICT)
