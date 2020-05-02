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

# The cleaning is done this way to reduce reptitive steps, whilst also allowing for some
# of the messiness in the data, which means every file cannot be processed exactly
# the same way. 

# One dataframe per variable theme is saved out to the cleaned folder. 

#++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create dictionary of specifications for each variable
#++++++++++++++++++++++++++++++++++++++++++++++++++++++

# example_dict = {
#         "data": raw.DATANAME,
#         "res": 'LSOA' OR 'LA',
#         "key_col": , #name of col which is the key,
#         "key_is_code": , #bool of whether the key is a code, if not it is a name 
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
        "outname": 'welsh_speakers_percent'
        }
        
lsoa_population_dict = {
        "data": raw.POPULATION_LSOA,
        "res": 'LSOA',
        "code_col": "Area Codes",
        "rename_dict": {'All Ages': 'population_count'},
        "keep_cols": []
        }

lsoa_over_65_dict = {
        "data": raw.OVER_65_LSOA,
        "res": 'LSOA',
        "code_col": "Area Codes",
        "rename_dict": None,
        "keep_cols": []
        }

lsoa_imd_dict = {
        "data": raw.IMD_LSOA,
        "code_col": "lsoa11cd",
        "rename_dict": {},
        "keep_cols": ['LSOA11CD', 'wimd_2019']
        }

lsoa_popdensity_dict = {
        "data": raw.POPDENSITY_LSOA,
        "code_col": "Code",
        "rename_dict": {'People per Sq Km': 'pop_density_persqkm'},
        "keep_cols": ['LSOA11CD', 'pop_density_persqkm']
        }

la_vulnerable_dict = {
        "data": raw.VULNERABLE_LA,
        "res": "LA",
        "code_col": "index",
        "key_is_code": False,
        "rename_dict": {1: 'n',
                        38: 'vulnerable'},
        "bracketed_cols": ['vulnerable'],
        "keep_cols": []
        }

la_cohesion_dict = {
        "data": raw.COMM_COHESION_LA,
        "res": "LA",
        "code_col": "index",
        "key_is_code": False,
        "rename_dict": {1: 'n',
                        20: 'belonging_strong_agree',
                        21: 'belonging_agree'},
        "bracketed_cols": ['belonging_strong_agree', 'belonging_agree'],
        "keep_cols": [] 
        }

la_access_dict = {
        "data": raw.INTERNET_ACCESS_LA,
        "res": "LA",
        "code_col": "Unnamed: 0",
        "key_is_code": False,
        "rename_dict": {1: 'n',
                        20: 'belonging_strong_agree',
                        21: 'belonging_agree'},
        "bracketed_cols": ['belonging_strong_agree', 'belonging_agree'],
        "keep_cols": [] 
        }

la_internet_use_dict = {
        "data": raw.INTERNET_USE_LA,
        "res": "LA",
        "key_col": "Unnamed: 0",
        "key_is_code": False,
        "rename_dict": {1: 'n',
                        20: 'belonging_strong_agree',
                        21: 'belonging_agree'},
        "bracketed_cols": ['belonging_strong_agree', 'belonging_agree'],
        "keep_cols": [] 
        }

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Apply functions to each dataset, and create new constant
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++
WELSH_LSOA = clean_data(**lsoa_welsh_dict)

POPULATION_LSOA = clean_data(**lsoa_population_dict)









