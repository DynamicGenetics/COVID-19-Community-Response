# %% Import packages
import pandas as pd
import geopandas as gpd

# %% Read in the LSOA reference data
LSOA = gpd.read_file(
    "geoboundaries/boundaries_LSOA.geojson"
)
# %% Remove English data from LSOA
LSOA = LSOA[LSOA["LSOA11CD"].str.contains("W", na=False)]


# ++++++++
# WELSH
# ++++++++

# %% Read in the data
WELSH = pd.read_csv("raw/lsoa_welsh_language_2011.csv", usecols=[2, 3])

# %% Fix Welsh col names and drop rows with no LSOA code
WELSH.rename(
    columns={
        "Unnamed: 2": "LSOA11CD",
        "Percentage able to speak Welsh ": "percent_welsh_speakers",
    },
    inplace=True,
)
WELSH.dropna(subset=["LSOA11CD"], inplace=True)
# lastly, reset the index after dropping rows.
WELSH.reset_index(drop=True, inplace=True)

# %% Strip whitespace from LSOA11CD (ready to merge)
WELSH["LSOA11CD"] = WELSH["LSOA11CD"].apply(lambda x: x.strip())

# %% Join the Welsh speaking data with the LSOA
WELSH_CLEAN = LSOA.merge(welsh, on="LSOA11CD", how="inner")

# %% Write cleaned data to CSV with necessary columns
WELSH_CLEAN.to_csv(
    "cleaned/lsoa_welsh_speakers.csv",
    columns=["LSOA11CD", "LSOA11NM", "percent_welsh_speakers"],
    index=False,
)

# +++++++++++
# POULATION
# +++++++++++
# %%
POPULATION = pd.read_csv("raw/2019_pop.csv", usecols=[4, 7, 8], encoding="ISO-8859-1")

# +++++++++++++
# POP DENSITY
# +++++++++++++
# %%
# Read from Excel file, sheet index 3
POPDENSITY = pd.read_excel(
    "raw/mid2018_popdensity_engandwales.xlsx", sheet_name=3, usecols="A,B,E", skiprows=4
)


# ++++++
# IMD
# ++++++

# %%
IMD = pd.read_csv("raw/2019IMD_deciles.csv", usecols=[1, 2], encoding="ISO-8859-1")
