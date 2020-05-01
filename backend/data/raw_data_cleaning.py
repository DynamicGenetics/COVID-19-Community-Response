# %% Import packages
import pandas as pd
import geopandas as gpd

# %% Read in the LSOA reference data
LSOA = gpd.read_file(
    "static/geoboundaries/Lower_Layer_Super_Output_Areas_December_2011_Boundaries_EW_BSC.geojson"
)
# Keep only Welsh codes.
LSOA = clean_LSOAs(LSOA)



welsh_data = pd.read_csv("raw/lsoa_welsh_language_2011.csv", usecols=[2, 3])
population_data = = pd.read_excel("raw/lsoa_population_2018-19.xlsx",
                             sheet_name="Mid-2018 Persons", #Sheet 4
                             usecols="A, C, D, BR:CQ", #Reads columns - Area Codes, LSOA, All Ages, 65:90+
                             skiprows=4 # Data starts on row 5
                             )


WELSH = {
        "data": welsh_data,
        "LSOA11CD_col": 'Unnamed: 2',
        "rename_dict": {"Percentage able to speak Welsh ": "welsh_speakers_percent"},
        "keep_cols": {['LSOA11CD', 'welsh_speakers_percent']}
        }
        
POPULATION = {
        "data": population_data,
        "LSOA11CD_col": '"Area Codes",
        "rename_dict": 'All Ages': 'population_count',
        "keep_cols": {['LSOA11CD', 'population_count', 'over_65_count']}
        }
        


DATASETS = [WELSH, POPULATION, POPDENSITY, IMD]

for dataset in DATASETS:

# ++++++++
# WELSH
# ++++++++

# %% Apply functions
WELSH = clean_LSOAs(WELSH, LSOA11CD_col = 'Unnamed: 2')

# %% 
WELSH = tidy_LSOAs(WELSH, keep_cols=['LSOA11CD', 'welsh_speakers_percent'])

# +++++++++++
# POULATION (Creates total pop count and 65+ count)
# +++++++++++
# %% Read population level data
POPULATION = pd.read_excel("raw/lsoa_population_2018-19.xlsx",
                             sheet_name="Mid-2018 Persons", #Sheet 4
                             usecols="A, C, D, BR:CQ", #Reads columns - Area Codes, LSOA, All Ages, 65:90+
                             skiprows=4 # Data starts on row 5
                             )


# %% Sum columns of ages 65-90+
POPULATION['over_65_count']= POPULATION.iloc[:,3:].sum(axis=1)

# %% Rename columns
POPULATION.rename(columns={"Area Codes": "LSOA11CD",
                           'All Ages': 'population_count'}, inplace=True)

# %% Join on LSOA for accurate LSOA11NM
POPULATION_TIDY = LSOA[['LSOA11CD', 'LSOA11NM']].merge(POPULATION[['LSOA11CD', 'population_count', 'over_65_count']], on="LSOA11CD", how="inner")
# %% Read out population count
POPULATION_TIDY.to_csv(
    "cleaned/lsoa_population_count.csv",
    columns=["LSOA11CD", "LSOA11NM", "population_count"],
    index=False,
)

# %% Now read out over 65 to csv seperately. 
POPULATION_TIDY.to_csv(
    "cleaned/lsoa_over_65_count.csv",
    columns=["LSOA11CD", "LSOA11NM", "over_65_count"],
    index=False,
)

# +++++++++++++
# POP DENSITY
# +++++++++++++
# %%
# Read from Excel file, sheet index 3
POPDENSITY = pd.read_excel(
    "raw/lsoa_pop_density_2018-19.xlsx", sheet_name=3, usecols="A,B,E", skiprows=4
)


# ++++++
# IMD
# ++++++

# %%
IMD = pd.read_csv("raw/2019IMD_deciles.csv", usecols=[1, 2], encoding="ISO-8859-1")




