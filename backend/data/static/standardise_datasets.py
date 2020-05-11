"""Module that generates the cleaned datasets for each variable from raw"""

# Import packages
import pandas as pd
from dataclasses import dataclass

# Import functions from local module
from standardising_functions import clean_keys, standardise_keys, clean_bracketed_data

# Import the raw data constants
import source_datasets as s


@dataclass
class StandardiseData:
    """Class for mapping the changes needed to standardise each dataset"""

    data: pd.DataFrame
    res: str  # Resolution at 'LSOA' or 'LA'
    key_col: str  # Name of the column that has a unique key
    key_is_code: bool  # Is the key column a LA or LSOA code?
    csv_name: str  # Name for the output CSV
    keep_cols: list = []  # List of columns specifically wanted to keep
    bracketed_data_cols: list = None  # List of columns where data is in the format (DATA (PERCENT))
    rename: dict = None  # Dictionary of columns that need renaming Cleaningself('old_name' : 'new_name' }

    def standardise(self):
        """ Based on arguments provided, applies the correct functions to standardise the data.
        """
        # Filter the keycodes/names, remove whitespace, reset index
        df = clean_keys(
            df=self.data,
            res=self.res,
            key_col=self.key_col,
            key_is_code=self.key_is_code,
        )

        # Rename the columns as needed
        if self.rename:
            df.rename(columns=self.rename, inplace=True)

        # Merge against the LSOA dataset for consistent Codes and Names
        df_clean = standardise_keys(
            df=df, res=self.res, keep_cols=self.keep_cols, key_is_code=self.key_is_code
        )

        # If argument has been passed for bracketed_data_cols, then apply the function.
        if self.bracketed_data_cols:
            df_clean = clean_bracketed_data(df=df_clean, cols=self.bracketed_data_cols)

        # Write out to /cleaned
        # write_cleaned_data(df_clean, res=self.res, csv_name=self.csv_name)
        return df_clean


# ++++++++++++++++++++++++++++++++++++++
# Define each instance of the dataclass
# ++++++++++++++++++++++++++++++++++++++

LSOA_WELSH = StandardiseData(
    data=s.SOURCE_WELSH_LSOA,
    res="LSOA",
    key_col="Unnamed: 2",
    key_is_code=True,
    csv_name="welsh_speakers_percent",
    rename={"Percentage able to speak Welsh ": "welsh_speakers_percent"},
)

LA_WELSH = StandardiseData(
    data=s.SOURCE_WELSH_LA,
    res="LA",
    key_col="Unnamed: 1",
    key_is_code=False,
    csv_name="welsh_speakers_percent",
    rename={
        "Daily ": "welsh_daily_percent",
        "Weekly ": "welsh_weekly_percent",
        "Less Often ": "welsh_lessoften_percent",
    },
)

LSOA_POPULATION = StandardiseData(
    data=s.SOURCE_POPDENSITY_LSOA,
    res="LSOA",
    key_col="Area Codes",
    key_is_code=True,
    csv_name="population_count",
    rename={"All Ages": "population_count"},
)

LA_POPULATION = StandardiseData(
    data=s.SOURCE_POPULATION_LA,
    res="LA",
    key_col="Unnamed: 3",
    key_is_code=False,
    csv_name="population_count",
    rename={"All ages .1": "population_count"},
)

LSOA_OVER_65 = StandardiseData(
    data=s.SOURCE_OVER_65_LSOA,
    res="LSOA",
    key_col="Area Codes",
    key_is_code=True,
    csv_name="over_65_count",
)

LA_OVER_65 = StandardiseData(
    data=s.SOURCE_OVER_65_LA,
    res="LA",
    key_col="Unnamed: 3",
    key_is_code=False,
    csv_name="over_65_count",
    rename={"Unnamed: 14": "over_65_count"},
)

LSOA_IMD = StandardiseData(
    data=s.SOURCE_IMD_LSOA,
    res="LSOA",
    key_col="lsoa11cd",
    key_is_code=True,
    csv_name="wimd_2019",
    keep_cols=["LSOA11CD", "wimd_2019"],
)

LA_IMD = StandardiseData(
    data=s.SOURCE_IMD_LA,
    res="LA",
    key_col="Unnamed: 0",
    key_is_code=False,
    csv_name="wimd_2019",
)

LSOA_POPDENSITY = StandardiseData(
    data=s.SOURCE_POPDENSITY_LSOA,
    res="LSOA",
    key_col="Code",
    key_is_code=True,
    rename={"People per Sq Km": "pop_density_persqkm"},
    keep_cols=["LSOA11CD", "pop_density_persqkm"],
    csv_name="pop_density_persqkm",
)

LA_POPDENSITY = StandardiseData(
    data=s.SOURCE_POPDENSITY_LA,
    res="LA",
    key_col="Unnamed: 1",
    key_is_code=False,
    rename={"Mid-year 2018 ": "pop_density_persqkm"},
    csv_name="pop_density_persqkm",
)

LA_VULNERABLE = StandardiseData(
    data=s.SOURCE_VULNERABLE_LA,
    res="LA",
    key_col="index",
    key_is_code=False,
    rename={38: "vulnerable"},
    bracketed_data_cols=["vulnerable"],
    csv_name="vulnerable_count_percent",
)

LA_COHESION = StandardiseData(
    data=s.SOURCE_COMM_COHESION_LA,
    res="LA",
    key_col="index",
    key_is_code=False,
    rename={20: "belong_strongagree", 21: "belong_agree"},
    bracketed_data_cols=["belong_strongagree", "belong_agree"],
    csv_name="comm_cohesion_count_percent",
)

LA_INTERNET_ACCESS = StandardiseData(
    data=s.SOURCE_INTERNET_ACCESS_LA,
    res="LA",
    key_col="Unnamed: 0",
    key_is_code=False,
    rename={"Yes (%)": "has_internet_percent"},
    csv_name="has_internet_percent",
)

LA_INTERNET_USE = StandardiseData(
    data=s.SOURCE_INTERNET_USE_LA,
    res="LA",
    key_col="Unnamed: 0",
    key_is_code=False,
    rename={
        "Several times a day (%)": "use_several_daily_percent",
        "Daily (%) ": "use_daily_percent",
    },
    csv_name="use_internet_percent",
)

LA_ETHNICITY = StandardiseData(
    data=s.SOURCE_ETHNICITY_LA,
    res="LA",
    key_col="Unnamed: 1",
    key_is_code=False,
    csv_name="ethnicities_percent",
)

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Apply functions to each dataset, and create new constant
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# WELSH_LSOA = clean_data(LSOA_WELSH) -> WELSH_LSOA.standardise()
# WELSH_LA = clean_data(LA_WELSH)
# POPULATION_LSOA = clean_data(LSOA_POPDENSITY)
# POPULATION_LA = clean_data(LA_POPULATION)
# OVER_65_LSOA = clean_data(LSOA_OVER_65)
# OVER_65_LA = clean_data(LA_OVER_65)
# IMD_LSOA = clean_data(LSOA_IMD)
# IMD_LA = clean_data(LA_IMD)
# POPDENSITY_LSOA = clean_data(LSOA_POPDENSITY)
# POPDENSITY_LA = clean_data(LA_POPDENSITY)
# VULNERABLE_LA = clean_data(LA_VULNERABLE)
# COMM_COHESION_LA = clean_data(LA_COHESION)
# INTERNET_ACCESS_LA = clean_data(LA_INTERNET_ACCESS)
# INTERNET_USE_LA = clean_data(LA_INTERNET_USE)
# ETHNICITY_LA = clean_data(LA_ETHNICITY)
