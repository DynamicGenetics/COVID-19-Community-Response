# Import packages
import pandas as pd
import geopandas as gpd

# Import functions from local module 
from data_cleaning_functions import clean_codes, rename_cols, tidy_LSOAs, write_cleaned_data

#++++++++++++++++++++++++++
# What does this script do?
#+++++++++++++++++++++++++++

# It reads in each file from the raw/folder in turn.
# Some files in this folder contain mutiple data columns so these are seperated out 
# for clarity to different constants. 
# Some files unergo some inital transformation before the cleaning functions are applied. 
# The requirements for the cleaning functions are saved to a dict for each dataset
# and then the for loop at the end applies these to each dataframe. 

# The cleaning is done this way to reduce reptitive steps, whilst also allowing for some
# of the messiness in the data, which means every file cannot be processed exactly
# the same way. 

# One dataframe per variable theme is saved out to the cleaned folder. 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Read in and clean the data being used as ground truth for names
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Read in the LSOA reference data
LSOA = gpd.read_file(
    "static/geoboundaries/Lower_Layer_Super_Output_Areas_December_2011_Boundaries_EW_BSC.geojson"
)
# Keep only Welsh codes.
LSOA = clean_codes(LSOA, code_col='LSOA11CD', res='LSOA')

# Read in the LA reference data (should not require cleaning)
LA = gpd.read_file(
    "static/geoboundaries/Local_Authority_Districts_(December_2019)_Boundaries_UK_BGC.geojson"
)
LA = clean_codes(LA, code_col='lad19cd', res='LA')

#++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Read in the data and alter to most acceptable format
#++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Read Welsh Data
WELSH_LSOA = pd.read_csv("raw/lsoa_welsh_language_2011.csv", usecols=[2, 3])

# Read Population data (includes age based data)
population_data = pd.read_excel("raw/lsoa_population_2018-19.xlsx",
                             sheet_name="Mid-2018 Persons", #Sheet 4
                             usecols="A, C, D, BR:CQ", #Reads columns - Area Codes, LSOA, All Ages, 65:90+
                             skiprows=4 # Data starts on row 5
                             )
# Seperate population and age data to different dataframes
POPULATION_LSOA = population_data.iloc[:, [0, 1, 2]].copy()
OVER_65_LSOA = population_data.drop(columns='All Ages').copy()

# Read in IMD data 
IMD_LSOA = pd.read_csv("raw/lsoa_IMD_2019.csv")

# Read in population density data 
POPDENSITY_LSOA = pd.read_excel(
    "raw/lsoa_pop_density_2018-19.xlsx",
    sheet_name=3,
    usecols="A,B,E",
    skiprows=4
)

# Read in Vulnerable and Community Cohesion Data
vulnerable_and_cohesion = pd.read_excel("raw/la_vulnerableProxy_and_cohesion.xlsx",
                             sheet_name="By local authority", #Sheet 4
                             )
# Select only the columns of interest and transpose
vulnerable_and_cohesion = vulnerable_and_cohesion.iloc[[1, 20, 21, 38]].T
# Reset index so the LA name isn't the index
vulnerable_and_cohesion.reset_index(inplace=True)
#Seperate this dataframe out so it only contains one variable per dataframe
VULNERABLE_LA = vulnerable_and_cohesion.iloc[:, [0, 1, 4]].copy()
COMM_COHESION_LA = vulnerable_and_cohesion.iloc[:, [0, 1, 2, 3]].copy()


INTERNET_ACCESS_LA = pd.read_excel(
    "raw/National Survey results - internet use and freqency of access by local authority.xlsx",
    usecols="A,B",
    skiprows=4, # Data starts on row 5
    nrows=22 #Only parse 23 rows as there is more data underneath
)

INTERNET_USE_LA = pd.read_excel(
    "raw/National Survey results - internet use and freqency of access by local authority.xlsx",
    usecols="A,B,C",
    skiprows=34, # Data starts on row 5
    nrows=22 #Only parse 23 rows as there is more data underneath
)
# As some values have been withheld (but should add to 100), infer them from the other two 
INTERNET_USE_LA['WEEKLY_OR_LESS_PCT'] = 100 - INTERNET_USE_LA.iloc[:,2] - INTERNET_USE_LA.iloc[:,1]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Create dictionary of specifications for each variable
#++++++++++++++++++++++++++++++++++++++++++++++++++++++

lsoa_welsh_dict = {
        "data": WELSH_LSOA,
        "res": 'LSOA',
        "code_col": 'Unnamed: 2',
        "rename_dict": {"Percentage able to speak Welsh ": "welsh_speakers_percent"},
        "keep_cols": []
        }
        
lsoa_population_dict = {
        "data": POPULATION_LSOA,
        "res": 'LSOA',
        "code_col": "Area Codes",
        "rename_dict": {'All Ages': 'population_count'},
        "keep_cols": []
        }

lsoa_over_65_dict = {
        "data": OVER_65_LSOA,
        "res": 'LSOA',
        "code_col": "Area Codes",
        "rename_dict": None,
        "keep_cols": []
        }

lsoa_popdensity_dict = {
        "data": POPDENSITY_LSOA,
        "code_col": "Code",
        "rename_dict": {'People per Sq Km': 'pop_density_persqkm'},
        "keep_cols": ['LSOA11CD', 'pop_density_persqkm']
        }

lsoa_imd_dict = {
        "data": IMD_LSOA,
        "code_col": "lsoa11cd",
        "rename_dict": {},
        "keep_cols": ['LSOA11CD', 'wimd_2019']
        }

la_vulnerable_dict = {
        "data": VULNERABLE,
        "res": "LA",
        "code_col": "index",
        "key_is_code": False,
        "rename_dict": {1: 'n',
                        38: 'vulnerable'},
        "bracketed_cols": ['vulnerable'],
        "keep_cols": []
        }

la_cohesion_dict = {
        "data": COMM_COHESION,
        "res": "LA",
        "code_col": "index",
        "key_is_code": False,
        "rename_dict": {1: 'n',
                        20: 'belonging_strong_agree',
                        21: 'belonging_agree'},
        "bracketed_cols": ['belonging_strong_agree', 'belonging_agree'],
        "keep_cols": [] 
        }

la_internet_use_dict = {
        "data": INTERNET_USE_LA,
        "res": "LA",
        "code_col": "Unnamed: 0",
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
    # Filter the LSOAS, remove whitespace, reset index
    dataset = clean_codes(dataset, code_col=dataset.get('code_col'))
    # Rename the columns as needed
    rename_cols(dataset, rename=dataset.get('rename_dict'))
    # Merge against the LSOA dataset for consistent Codes and Names
    dataset_tidied = tidy_LSOAs(dataset, keep_cols=dataset.get('keep_cols'))
    # Write out to /cleaned
    write_cleaned_data(dataset_tidied)






ETHNICITY = 



