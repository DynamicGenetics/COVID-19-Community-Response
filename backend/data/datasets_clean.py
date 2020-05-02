# Import packages
import pandas as pd
import geopandas as gpd

# Import functions from local module 
from data_cleaning_functions import clean_data

# Import the data constants from local module
import datasets_raw as raw

#++++++++++++++++++++++++++
# What does this script do?
#+++++++++++++++++++++++++++
# The requirements for the cleaning functions are saved to a dict for each dataset
# and the constant definitions calls these to be applied to the raw constants. 
# Data is saved out to /cleaned

#++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create dictionary of specifications for each variable
#++++++++++++++++++++++++++++++++++++++++++++++++++++++

# example_dict = {
#         "data": raw.DATANAME,
#         "res": 'LSOA' OR 'LA',
#         "key_col": , #name of col which is the key,
#         "key_is_code": , #bool of whether the key is a code, if not it is a name 
#         "keep_cols": [] for all, or a list of columns you specifically want to keep in the cleaned df.
#         "csv_name": name of csv (resolution not needed)
#optional "bracketed_data_cols": ,  #list of cols where there data in the format (DATA (PERCENT))
#optional "rename_dict": , #dictionary of columns that need renaming
#          }

lsoa_welsh_dict = {
        "data": raw.WELSH_LSOA,
        "res": 'LSOA',
        "key_col": 'Unnamed: 2',
        "key_is_code": True,
        "rename_dict": {"Percentage able to speak Welsh ": "welsh_speakers_percent"},
        "keep_cols": [],
        "csv_name": 'welsh_speakers_percent'
        }
        
lsoa_population_dict = {
        "data": raw.POPULATION_LSOA,
        "res": 'LSOA',
        "key_col": "Area Codes",
        "key_is_code": True,
        "rename_dict": {'All Ages': 'population_count'},
        "keep_cols": [],
        "csv_name": 'population_count'
        }

lsoa_over_65_dict = {
        "data": raw.OVER_65_LSOA,
        "res": 'LSOA',
        "key_col": "Area Codes",
        "key_is_code": True,
        "keep_cols": [],
        "csv_name": 'over_65_count'
        }

lsoa_imd_dict = {
        "data": raw.IMD_LSOA,
        "res": 'LSOA',
        "key_col": "lsoa11cd",
        "key_is_code": True,
        "keep_cols": ['LSOA11CD', 'wimd_2019'],
        "csv_name": 'wimd_2019'
        }

lsoa_popdensity_dict = {
        "data": raw.POPDENSITY_LSOA,
        "res": 'LSOA',
        "key_col": "Code",
        "key_is_code": True,
        "rename_dict": {'People per Sq Km': 'pop_density_persqkm'},
        "keep_cols": ['LSOA11CD', 'pop_density_persqkm'],
        "csv_name": 'pop_density_persqkm'
        }

la_vulnerable_dict = {
        "data": raw.VULNERABLE_LA,
        "res": "LA",
        "key_col": "index",
        "key_is_code": False,
        "rename_dict": {1: 'n',
                        38: 'vulnerable'},
        "bracketed_data_cols": ['vulnerable'],
        "keep_cols": [],
        "csv_name": 'vulnerable_count_percent'
        }

la_cohesion_dict = {
        "data": raw.COMM_COHESION_LA,
        "res": "LA",
        "key_col": "index",
        "key_is_code": False,
        "rename_dict": {1: 'n',
                        20: 'belong_strongagree',
                        21: 'belong_agree'},
        "bracketed_data_cols": ['belong_strongagree', 'belong_agree'],
        "keep_cols": [],
        "csv_name": 'comm_cohesion_count_percent'
        }

la_internet_access_dict = {
        "data": raw.INTERNET_ACCESS_LA,
        "res": "LA",
        "key_col": "Unnamed: 0",
        "key_is_code": False,
        "rename_dict": {'Yes (%)': 'has_internet_percent'},
        "keep_cols": [],
        "csv_name": 'has_internet_percent'
        }

la_internet_use_dict = {
        "data": raw.INTERNET_USE_LA,
        "res": "LA",
        "key_col": "Unnamed: 0",
        "key_is_code": False,
        "rename_dict": {'Several times a day (%)': 'use_several_daily_percent',
                        'Daily (%) ': 'use_daily_percent'},
        "keep_cols": [],
        "csv_name": 'use_internet_percent'
        }

la_ethnicity_dict = {
        "data": ETHNICITY_LA,
        "res": "LA",
        "key_col": "Unnamed: 1",
        "key_is_code": False,
        "keep_cols": [],
        "csv_name": 'ethnicities_percent'
}

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Apply functions to each dataset, and create new constant
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
WELSH_LSOA = clean_data(**lsoa_welsh_dict)

POPULATION_LSOA = clean_data(**lsoa_population_dict)

OVER_65_LSOA = clean_data(**lsoa_over_65_dict)

IMD_LSOA = clean_data(**lsoa_imd_dict)

POPDENSITY_LSOA = clean_data(**lsoa_popdensity_dict)

VULNERABLE_LA = clean_data(**la_vulnerable_dict)

COMM_COHESION_LA = clean_data(**la_cohesion_dict)

INTERNET_ACCESS_LA = clean_data(**la_internet_access_dict)

INTERNET_USE_LA = clean_data(**la_internet_use_dict)

ETHNICITY_LA = clean_data(**la_ethnicity_dict)