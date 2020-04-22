# %% Import packages
import pandas as pd
import geopandas as gpd

# %% Read in the LSOA reference data
lsoa = gpd.read_file("../geography/boundaries_LSOAs.geojson")
# %% Remove English data from lsoa
lsoa = lsoa[lsoa['LSOA11CD'].str.contains("W", na=False)]


#++++++++
# WELSH 
#++++++++

# %% Read in the data
welsh = pd.read_csv("lsoa_welsh_language_2011.csv",
                    usecols=[2, 3])

# %% Fix Welsh col names and drop rows with no LSOA code
welsh.rename(columns={'Unnamed: 2': 'LSOA11CD'}, inplace=True)
welsh.dropna(subset=['LSOA11CD'], inplace=True)


#+++++++++++
# POULATION
#+++++++++++
# %%
population = pd.read_csv("2019_pop.csv", usecols=[4, 7, 8], encoding="ISO-8859-1")

#+++++++++++++
# POP DENSITY
#+++++++++++++
# %%
# Read from Excel file, sheet index 3
popdensity = pd.read_excel("mid2018_popdensity_engandwales.xlsx", sheet_name=3, usecols="A,B,E", skiprows=4)


#++++++
# IMD
#++++++

# %%
imd = pd.read_csv("2019IMD_deciles.csv", usecols=[1, 2], encoding="ISO-8859-1")

