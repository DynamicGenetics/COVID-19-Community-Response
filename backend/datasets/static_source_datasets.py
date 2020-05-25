"""Handles reading of datasets from source folder"""

import pandas as pd
import os
from functools import partial

# ++++++++++++++++++++++++++++++++++
# Read data into acceptable format
# ++++++++++++++++++++++++++++++++++
from datasets import SOURCE_DATA_FOLDER

# Base folders for all Source Files
p = partial(os.path.join, SOURCE_DATA_FOLDER)

SOURCE_SHEILDING_LA = pd.read_csv(p("shielded_pop_LA.csv"))

SOURCE_WELSH_LSOA = pd.read_csv(p("lsoa_welsh_language_2011.csv"), usecols=[2, 3])

SOURCE_WELSH_LA = pd.read_csv(
    p("la_welsh_frequency_2018-19.csv"), usecols=[1, 2, 3, 4], na_values="*"
)


# Read Population data (includes age based data)
SOURCE_POPULATION_LSOA = pd.read_excel(
    p("lsoa_population_2018-19_mid_2018_persons.xlsx"),
    usecols="A, D",  # Reads columns - Area Codes, All Ages
    skiprows=4,  # Data starts on row 5
    na_filter=False,  # Speed up read in of data, we know there are no NA values here
)

SOURCE_OVER_65_LSOA = pd.read_excel(
    p("lsoa_population_2018-19_mid_2018_persons.xlsx"),
    usecols="A, BR:CQ",  # Reads columns - Area Codes, 65:90+
    skiprows=4,  # Data starts on row 5
    na_filter=False,  # Speed up read in of data, we know there are no NA values here
)

SOURCE_POPULATION_LA = pd.read_csv(p("la_population_age_2019.csv"), usecols=[3, 15])
SOURCE_OVER_65_LA = pd.read_csv(p("la_population_age_2019.csv"), usecols=[3, 14])


# Read in IMD data
SOURCE_IMD_LSOA = pd.read_csv(p("lsoa_IMD_2019.csv"))

SOURCE_IMD_LA = pd.read_csv(p("la_WIMD_2019.csv"))

# Read in population density data
SOURCE_POPDENSITY_LSOA = pd.read_excel(
    p("lsoa_pop_density_2018-19.xlsx"), sheet_name=3, usecols="A,B,E", skiprows=4
)

SOURCE_POPDENSITY_LA = pd.read_csv(p("la_pop_density_2018.csv"), usecols=[1, 11])

# Read in Vulnerable and Community Cohesion Data
vulnerable_and_cohesion = pd.read_excel(
    p("la_vulnerableProxy_and_cohesion.xlsx"),
    sheet_name="By local authority",
    usecols="B:X",
)
# Select only the columns of interest and transpose
vulnerable_and_cohesion = vulnerable_and_cohesion.iloc[[1, 20, 21, 38]].T
# Reset index so the LA name isn't the index
vulnerable_and_cohesion.reset_index(inplace=True)
# Seperate this dataframe out so it only contains one variable per dataframe
SOURCE_VULNERABLE_LA = vulnerable_and_cohesion.iloc[:, [0, 4]].copy()
SOURCE_COMM_COHESION_LA = vulnerable_and_cohesion.iloc[:, [0, 2, 3]].copy()


SOURCE_INTERNET_ACCESS_LA = pd.read_excel(
    p(
        "National Survey results - internet use and freqency of access by local authority.xlsx"
    ),
    usecols="A,B",
    skiprows=4,  # Data starts on row 5
    nrows=22,  # Only parse 22 rows as there is more data underneath
)

SOURCE_GP_ONLINE_LA = pd.read_csv(p("la_gp_online.csv"))

# -------------------------
# Currently unused datasets
# --------------------------

# SOURCE_INTERNET_USE_LA = pd.read_excel(
#     p(
#         "National Survey results - internet use and freqency of access by local authority.xlsx"
#     ),
#     usecols="A,B,C",
#     skiprows=34,  # Data starts on row 5
#     nrows=22,  # Only parse 22 necessary rows
# )

# This data is formatted the wrong way in the spreadsheet so needs extra work
# SOURCE_ETHNICITY_LA = pd.read_excel(
#     p("la_lhb_ethnicity.xlsx"), sheet_name="By Local Authority", usecols="B:X"
# ).T
# SOURCE_ETHNICITY_LA.reset_index(inplace=True)
# SOURCE_ETHNICITY_LA.rename(columns=SOURCE_ETHNICITY_LA.iloc[0], inplace=True)
# SOURCE_ETHNICITY_LA.drop(SOURCE_ETHNICITY_LA.index[0], inplace=True)
# SOURCE_ETHNICITY_LA.drop(SOURCE_ETHNICITY_LA.columns[1], axis=1, inplace=True)
