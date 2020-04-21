# %% Import packages
import pandas as pd
import geopandas as gpd

# %% Read in the data
welsh = pd.read_csv("2011census_welsh_lang.csv",
                    usecols=[2, 3], skiprows=8)
population = pd.read_csv("2019_pop.csv", usecols=[4, 7, 8], encoding="ISO-8859-1")
imd = pd.read_csv("2019IMD_deciles.csv", usecols=[1, 2], encoding="ISO-8859-1")
# Read from Excel file, sheet index 3
popdensity = pd.read_excel("mid2018_popdensity_engandwales.xlsx", sheet_name=3, usecols="A,B,E", skiprows=4)

lsoa = gpd.read_file("../geography/boundaries_LSOAs.geojson")

# %%
