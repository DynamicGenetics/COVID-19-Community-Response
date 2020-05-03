import pandas

# ++++++++++++++++++++++++++++++++++
# Read data into acceptable format
# ++++++++++++++++++++++++++++++++++
# Some datasets have variables which need to be added up to get the right data.

POPULATION_LSOA = pd.read_csv()

# Crate new 'over 65' variable for the population data (adding up all singlar age cols from 65:90+)
POPULATION_LSOA["over_65_count"] = POPULATION_LSOA.iloc[:, 3:].sum(axis=1)

# Get the sum of the people who use the internet daily
INTERNET_USE_LA["use_internet_daily_percent"] = (
    INTERNET_USE_LA.iloc[:, 2] + INTERNET_USE_LA.iloc[:, 1]
)

# Get the sum of the people who do use Welsh at all
WELSH_LA["use_welsh_percent"] = (
    WELSH_LA["Daily "] + WELSH_LA["Weekly "] + WELSH_LA["Less Often "]
)

# Create summary ethnicity columns by summing groups
ETHNICITY_LA["White"] = ETHNICITY_LA.filter(regex=("^White")).sum(axis=1)
ETHNICITY_LA["Asian"] = ETHNICITY_LA.filter(regex=("^Asian")).sum(axis=1)
ETHNICITY_LA["Black"] = ETHNICITY_LA.filter(regex=("^Black")).sum(axis=1)
ETHNICITY_LA["Mixed"] = ETHNICITY_LA.filter(regex=("^Mixed")).sum(axis=1)
ETHNICITY_LA["Other"] = ETHNICITY_LA.filter(regex=("^Other")).sum(axis=1)
