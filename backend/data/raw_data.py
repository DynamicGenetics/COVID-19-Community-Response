"""
 Handles the import of raw datasets
"""

import pandas as pd
import geopandas as gpd
from dataclasses import dataclass
from functools import partial
import os

DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static", "raw")


p = partial(os.path.join, DATA_FOLDER)

# ++++++++++++++++++++++++++++++++++
# Read data into acceptable format
# ++++++++++++++++++++++++++++++++++


class RawDataset:
    """A class for handling import of raw datasets
    """

    SUPPORTED_FORMATS = {
        "csv": pd.read_csv,
        "xlsx": pd.read_excel,
        "geojson": gpd.read_file,
        "no-format": lambda f: None,  # dummy
    }

    def __init__(self, filepath: str, **extra_pars: dict):
        self._filepath = filepath
        self._data_format = self._guess_data_format(self._filepath)
        self._read_fn = self.SUPPORTED_FORMATS[self._data_format]
        self._read_fn_params = extra_pars
        self._data = None  # actual placeholder for the dataset

    def _guess_data_format(self, filepath: str):
        _, ext = os.path.splitext(filepath)
        ext = ext[1:].lower()  # get rid of initial dot
        if ext in self.SUPPORTED_FORMATS:
            return ext
        return "no-format"

    # @property
    # def source_path(self):
    #     try:  # BTAFTP
    #         data_path = os.path.join(DATA_FOLDER, self._filename)
    #         with open(data_path) as _:
    #             pass
    #     except FileNotFoundError:
    #         raise FileNotFoundError(f'Data source "{self._filename}" does not exist.')
    #     else:
    #         return data_path

    @property
    def is_valid(self):
        try:
            with open(self._filepath) as _:
                pass
        except FileNotFoundError:
            return False
        else:
            return True

    @property
    def data(self):
        if not self.is_valid:
            return None
        if self._data is None:
            self._data = self._read_fn(self._filepath, **self._read_fn_params)
        return self._data


RAW_WELSH_LSOA = RawDataset(filepath=p("lsoa_welsh_language_2011.csv"), usecols=[2, 3])


RAW_WELSH_LA = RawDataset(
    filepath=p("la_welsh_frequency_2018-19.csv"), usecols=[1, 2, 3, 4]
)


# Read Population data (includes age based data)
RAW_POPULATION_LSOA = RawDataset(
    filepath=p("lsoa_population_2018-19.xlsx"),
    sheet_name="Mid-2018 Persons",  # Sheet 4
    usecols="A, D",  # Reads columns - Area Codes, All Ages
    skiprows=4,  # Data starts on row 5
)

RAW_OVER_65_LSOA = RawDataset(
    filepath=p("lsoa_population_2018-19.xlsx"),
    sheet_name="Mid-2018 Persons",  # Sheet 4
    usecols="A, BR:CQ",  # Reads columns - Area Codes, 65:90+
    skiprows=4,  # Data starts on row 5
)

RAW_POPULATION_LA = RawDataset(
    filepath=p("la_population_age_2019.csv"), usecols=[3, 15]
)
RAW_OVER_65_LA = RawDataset(filepath=p("la_population_age_2019.csv"), usecols=[3, 14])


# Read in IMD data
RAW_IMD_LSOA = RawDataset(filepath=p("lsoa_IMD_2019.csv"))

RAW_IMD_LA = RawDataset(filepath=p("la_WIMD_2019.csv"))

# Read in population density data
RAW_POPDENSITY_LSOA = RawDataset(
    filepath=p("lsoa_pop_density_2018-19.xlsx"),
    sheet_name=3,
    usecols="A,B,E",
    skiprows=4,
)

RAW_POPDENSITY_LA = RawDataset(filepath=p("la_pop_density_2018.csv"), usecols=[1, 11])

# Read in Vulnerable and Community Cohesion Data
VULNERABLE_AND_COHESION = RawDataset(
    filepath=p("la_vulnerableProxy_and_cohesion.xlsx"),
    sheet_name="By local authority",
    usecols="B:X",
)

# Select only the columns of interest and transpose
VULNERABLE_AND_COHESION = VULNERABLE_AND_COHESION.data.iloc[
    [1, 20, 21, 38]
].T.reset_index(inplace=True)
# Reset index so the LA name isn't the index
VULNERABLE_AND_COHESION
# Seperate this dataframe out so it only contains one variable per dataframe
RAW_VULNERABLE_LA = VULNERABLE_AND_COHESION.iloc[:, [0, 4]].copy()
RAW_COMM_COHESION_LA = VULNERABLE_AND_COHESION.iloc[:, [0, 2, 3]].copy()


RAW_INTERNET_ACCESS_LA = RawDataset(
    filepath=p(
        "National Survey results - internet use and freqency of access by local authority.xlsx"
    ),
    usecols="A,B",
    skiprows=4,  # Data starts on row 5
    nrows=22,  # Only parse 22 rows as there is more data underneath
)

# NB Here we aren't reading in the last column, because it is half empty.
RAW_INTERNET_USE_LA = RawDataset(
    filepath=p(
        "National Survey results - internet use and freqency of access by local authority.xlsx"
    ),
    usecols="A,B,C",
    skiprows=34,  # Data starts on row 5
    nrows=22,  # Only parse 22 necessary rows
)

# This data is formatted the wrong way in the spreadsheet so needs extra work
RAW_ETHNICITY_LA = RawDataset(
    filepath=p("la_lhb_ethnicity.xlsx"), sheet_name="By Local Authority", usecols="B:X"
).T
RAW_ETHNICITY_LA.reset_index(inplace=True)
RAW_ETHNICITY_LA.rename(columns=RAW_ETHNICITY_LA.iloc[0], inplace=True)
RAW_ETHNICITY_LA.drop(RAW_ETHNICITY_LA.index[0], inplace=True)
RAW_ETHNICITY_LA.drop(RAW_ETHNICITY_LA.columns[1], axis=1, inplace=True)
