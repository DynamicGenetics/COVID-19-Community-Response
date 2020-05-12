"""Handles reading of datasets from source folder"""

import pandas as pd
import geopandas as gpd
import os
from functools import partial
from enum import Enum

# ++++++++++++++++++++++++++
# What does this script do?
# +++++++++++++++++++++++++++
# It reads in each file from the source/folder in turn.
# Some files in this folder contain mutiple data columns so these are seperated out
# to different dataframe constants for clarity.

from datasets import SOURCE_DATA_FOLDER

# Base folder for all Source Files
p = partial(os.path.join, SOURCE_DATA_FOLDER)


class DataFormats(Enum):
    CSV = pd.read_csv
    XLS = pd.read_excel
    JSON = pd.read_json
    GEOJSON = gpd.read_file


FORMAT_EXTENSIONS = {
    ".csv": DataFormats.CSV,
    ".xls": DataFormats.XLS,
    ".xlsx": DataFormats.XLS,
    ".json": DataFormats.JSON,
}


class SourceDataset:
    """This class encapsulate the logic of a Source (static) Dataset
    as generated from a local data file.
    Supported formats for data files are: CSV, Excel, JSON,
    GeoJSon (using GeoPandas).

    Internal data representation is build on `pandas.DataFrame`
    (`geopandas.GeoDataFrame` for geojson files).

    Data is loaded
    (1) in a lazy fashion, deferring the actual loading of
        data files when it is required,
    (2) just once, so saving and re-using the reference to the data
        for future calls.
    The format of the data to load will be automatically deferred from

    To allow for lazy deferred loading, extra operations
    """

    UNKNOWN_FORMAT = "unknown"

    SUPPORTED_FORMATS = {
        "csv": pd.read_csv,
        "xlsx": pd.read_excel,
        "json": pd.read_json,
        "geojson": gpd.read_file,
        UNKNOWN_FORMAT: lambda f: None,
    }

    def __init__(self, filepath: str, data_format: str, **read_fn_params):
        self._filepath = filepath
        self._data_format = self._infer_format(filepath)
        self._data = None  # Lazy loading
        self._read_fn = self.SUPPORTED_FORMATS[self._data_format]
        self._read_fn_params = (
            read_fn_params if not self._data_format == self.UNKNOWN_FORMAT else {}
        )

    def _infer_format(self, filepath):
        _, ext = os.path.splitext(filepath)
        ext = ext[1:]  # get rid of "."
        try:
            fmt = ext
        except KeyError:
            fmt = self.UNKNOWN_FORMAT
        return fmt

    @property
    def data(self):
        if self._data is None:
            self._data = self._read_fn(self._filepath, **self._read_fn_params)
        return self._data


SOURCE_WELSH_LSOA = SourceDataset(
    filepath=p("lsoa_welsh_language_2011.csv"), usecols=[2, 3]
)

# SOURCE_WELSH_LA = pd.read_csv(p("la_welsh_frequency_2018-19.csv"), usecols=[1, 2, 3, 4])
#
# # Read Population data (includes age based data)
# SOURCE_POPULATION_LSOA = pd.read_excel(
#     p("lsoa_population_2018-19.xlsx"),
#     sheet_name="Mid-2018 Persons",  # Sheet 4
#     usecols="A, D",  # Reads columns - Area Codes, All Ages
#     skiprows=4,  # Data starts on row 5
# )
#
# SOURCE_OVER_65_LSOA = pd.read_excel(
#     p("lsoa_population_2018-19.xlsx"),
#     sheet_name="Mid-2018 Persons",  # Sheet 4
#     usecols="A, BR:CQ",  # Reads columns - Area Codes, 65:90+
#     skiprows=4,  # Data starts on row 5
# )
#
# SOURCE_POPULATION_LA = pd.read_csv(p("la_population_age_2019.csv"), usecols=[3, 15])
# SOURCE_OVER_65_LA = pd.read_csv(p("la_population_age_2019.csv"), usecols=[3, 14])
#
# # Read in IMD data
# SOURCE_IMD_LSOA = pd.read_csv(p("lsoa_IMD_2019.csv"))
#
# SOURCE_IMD_LA = pd.read_csv(p("la_WIMD_2019.csv"))
#
# # Read in population density data
# SOURCE_POPDENSITY_LSOA = pd.read_excel(
#     p("lsoa_pop_density_2018-19.xlsx"), sheet_name=3, usecols="A,B,E", skiprows=4
# )
#
# SOURCE_POPDENSITY_LA = pd.read_csv(p("la_pop_density_2018.csv"), usecols=[1, 11])
#
# # Read in Vulnerable and Community Cohesion Data
# vulnerable_and_cohesion = pd.read_excel(
#     p("la_vulnerableProxy_and_cohesion.xlsx"),
#     sheet_name="By local authority",
#     usecols="B:X",  # Sheet 4
# )
# # Select only the columns of interest and transpose
# vulnerable_and_cohesion = vulnerable_and_cohesion.iloc[[1, 20, 21, 38]].T
# # Reset index so the LA name isn't the index
# vulnerable_and_cohesion.reset_index(inplace=True)
# # Seperate this dataframe out so it only contains one variable per dataframe
# SOURCE_VULNERABLE_LA = vulnerable_and_cohesion.iloc[:, [0, 4]].copy()
# SOURCE_COMM_COHESION_LA = vulnerable_and_cohesion.iloc[:, [0, 2, 3]].copy()
#
# SOURCE_INTERNET_ACCESS_LA = pd.read_excel(
#     p(
#         "National Survey results - internet use and freqency of access by local authority.xlsx"
#     ),
#     usecols="A,B",
#     skiprows=4,  # Data starts on row 5
#     nrows=22,  # Only parse 22 rows as there is more data underneath
# )
#
# # NB Here we aren't reading in the last column, because it is half empty.
# SOURCE_INTERNET_USE_LA = pd.read_excel(
#     p(
#         "National Survey results - internet use and freqency of access by local authority.xlsx"
#     ),
#     usecols="A,B,C",
#     skiprows=34,  # Data starts on row 5
#     nrows=22,  # Only parse 22 necessary rows
# )
#
# # This data is formatted the wrong way in the spreadsheet so needs extra work
# SOURCE_ETHNICITY_LA = pd.read_excel(
#     p("la_lhb_ethnicity.xlsx"), sheet_name="By Local Authority", usecols="B:X"
# ).T
# SOURCE_ETHNICITY_LA.reset_index(inplace=True)
# SOURCE_ETHNICITY_LA.rename(columns=SOURCE_ETHNICITY_LA.iloc[0], inplace=True)
# SOURCE_ETHNICITY_LA.drop(SOURCE_ETHNICITY_LA.index[0], inplace=True)
# SOURCE_ETHNICITY_LA.drop(SOURCE_ETHNICITY_LA.columns[1], axis=1, inplace=True)

if __name__ == "__main__":
    s = SOURCE_WELSH_LSOA
    print(s.data.head())
    df = pd.read_csv(p("lsoa_welsh_language_2011.csv"), usecols=[2, 3])
    print(pd.DataFrame.equals(s.data, df))
