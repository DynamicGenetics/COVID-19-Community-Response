# %% Import packages
import pandas as pd
import geopandas as gpd

# %% Read in the LSOA reference data
lsoa = gpd.read_file(
    "static/geoboundaries/Lower_Layer_Super_Output_Areas_December_2011_Boundaries_EW_BSC.geojson"
)
# %% Remove English data from lsoa
lsoa = lsoa[lsoa["LSOA11CD"].str.contains("W", na=False)]


# ++++++++
# WELSH
# ++++++++

# %% Read in the data
welsh = pd.read_csv("raw/lsoa_welsh_language_2011.csv", usecols=[2, 3])

# %% Fix Welsh col names and drop rows with no LSOA code
welsh.rename(
    columns={
        "Unnamed: 2": "LSOA11CD",
        "Percentage able to speak Welsh ": "percent_welsh_speakers",
    },
    inplace=True,
)
welsh.dropna(subset=["LSOA11CD"], inplace=True)
# lastly, reset the index after dropping rows.
welsh.reset_index(drop=True, inplace=True)

# %% Strip whitespace from LSOA11CD (ready to merge)
welsh["LSOA11CD"] = welsh["LSOA11CD"].apply(lambda x: x.strip())

# %% Join the Welsh speaking data with the LSOA
welsh_tidy = lsoa.merge(welsh, on="LSOA11CD", how="inner")

# %% Write cleaned data to CSV with necessary columns
welsh_tidy.to_csv(
    "cleaned/lsoa_welsh_speakers.csv",
    columns=["LSOA11CD", "LSOA11NM", "percent_welsh_speakers"],
    index=False,
)

# +++++++++++
# POULATION
# +++++++++++
# %%
population = pd.read_csv("raw/2019_pop.csv", usecols=[4, 7, 8], encoding="ISO-8859-1")

# +++++++++++++
# POP DENSITY
# +++++++++++++
# %%
# Read from Excel file, sheet index 3
popdensity = pd.read_excel(
    "raw/mid2018_popdensity_engandwales.xlsx", sheet_name=3, usecols="A,B,E", skiprows=4
)


# ++++++
# IMD
# ++++++

# %%
imd = pd.read_csv("raw/2019IMD_deciles.csv", usecols=[1, 2], encoding="ISO-8859-1")
