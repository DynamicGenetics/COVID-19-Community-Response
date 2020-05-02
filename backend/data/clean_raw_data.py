# Import packages
import pandas as pd
import geopandas as gpd

# Import functions from local module 
from data_cleaning_functions import clean_codes, standardise_keys, clean_bracketed_data, write_cleaned_data

# Import the data constants from raw.py
import raw

#++++++++++++++++++++++++++
# What does this script do?
#+++++++++++++++++++++++++++
# The requirements for the cleaning functions are saved to a dict for each dataset
# and then the for loop at the end applies these to each dataframe. 

# The cleaning is done this way to reduce reptitive steps, whilst also allowing for some
# of the messiness in the data, which means every file cannot be processed exactly
# the same way. 

# One dataframe per variable theme is saved out to the cleaned folder. 

#++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create dictionary of specifications for each variable
#++++++++++++++++++++++++++++++++++++++++++++++++++++++

# example_dict = {
#         "data": DATANAME,
#         "res": 'LSOA OR LA',
#         "key_col": , #name of col which is the key,
#         "key_is_code": , #bool of whether the key is a code, if not it is a name 
#         "bracketed_data_cols": ,  #list of cols where there data in the format (DATA (PERCENT))?
#         "rename_dict": , #dictionary of columns that need renaming
#         "keep_cols": , #list of columns to write out to CSV. If empty, assumes all.
#         "outname": . #core of file when being written to csv (resolution appended later)
# }

lsoa_welsh_dict = {
        "data": raw.WELSH_LSOA,
        "res": 'LSOA',
        "code_col": 'Unnamed: 2',
        "rename_dict": {"Percentage able to speak Welsh ": "welsh_speakers_percent"},
        "keep_cols": []
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
        "data": raw.VULNERABLE,
        "res": "LA",
        "code_col": "index",
        "key_is_code": False,
        "rename_dict": {1: 'n',
                        38: 'vulnerable'},
        "bracketed_cols": ['vulnerable'],
        "keep_cols": []
        }

la_cohesion_dict = {
        "data": raw.COMM_COHESION,
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
# Loop through the datasets, apply functions and save out
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++


lsoa_datasets = [lsoa_welsh_dict, lsoa_population_dict, lsoa_popdensity_dict, lsoa_imd_dict]
la_datasets=[]

for dataset in datasets:
    data = dataset.get("data")
    # Filter the LSOAS, remove whitespace, reset index
    data = clean_codes(data, key_col=dataset.get('key_col'))
    # Rename the columns as needed
    data.rename(columns=dataset.get('rename_dict'), inplace=True)
    # Merge against the LSOA dataset for consistent Codes and Names
    data_cleaned = tidy_LSOAs(data, keep_cols=dataset.get('keep_cols'))
    # Write out to /cleaned
    write_cleaned_data(data_cleaned)






ETHNICITY = 



