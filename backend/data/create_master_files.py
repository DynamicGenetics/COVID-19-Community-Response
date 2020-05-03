import pandas as pd
import os
from functools import reduce

# Set up directory for the os
directory = "cleaned/"

# Initialise some values for the loop
la = {}
i = 0

# Read in all the dataframes to a dictionary
for filename in os.listdir(directory):
    if filename.startswith("LA_"):
        la["df{}".format(i)] = pd.read_csv("cleaned/" + filename, index_col=[0, 1])
        i += 1  # Add one to the i constant
        continue
    else:
        continue

# Make a list of all the dataframes for the merge.
la_list = list(la.values())
# Merge all the dataframes on the indexes
la_master = reduce(
    lambda left, right: pd.merge(left, right, left_index=True, right_index=True),
    la_list,
)

# Now do the same for the lsoa!
# Initialise some values for the loop
lsoa = {}
j = 0

# Read in all the dataframes to a dictionary
for filename in os.listdir(directory):
    if filename.startswith("LSOA_"):
        lsoa["df{}".format(j)] = pd.read_csv("cleaned/" + filename, index_col=[0, 1])
        j += 1  # Add one to the i constant
        continue
    else:
        continue

# Make a list of all the dataframes for the merge.
lsoa_list = list(lsoa.values())
# Merge all the dataframes on the indexes
lsoa_master = reduce(
    lambda left, right: pd.merge(left, right, left_index=True, right_index=True),
    lsoa_list,
)


# ++++++++++++++++++++++++++++++++++
# Create some summary variables
# ++++++++++++++++++++++++++++++++++
# Some datasets have variables which need to be added up to get the right data.

# LSOA LEVEL VARBS
# Crate new 'over 65' variable for the population data (adding up all
# singlar age cols from 65:90+)
age_cols = lsoa_master.columns[
    pd.to_numeric(lsoa_master.columns, errors="coerce").to_series().notnull()
]
lsoa_master["over_65_count"] = lsoa_master[age_cols].sum(axis=1) + lsoa_master["90+"]
lsoa_master.drop(columns=age_cols, inplace=True)
lsoa_master.drop(columns="90+", inplace=True)

# Write out
lsoa_master.to_csv("cleaned/master_static_LSOA.csv")


# LA LEVEL VARBS
# Get the sum of the people who use the internet daily
internet_use_cols = ["use_daily_percent", "use_several_daily_percent"]
la_master["use_internet_daily_percent"] = la_master[internet_use_cols].sum(axis=1)
la_master.drop(columns=internet_use_cols, inplace=True)

# Get the sum of the people who do use Welsh at all
welsh_cols = ["welsh_daily_percent", "welsh_weekly_percent", "welsh_lessoften_percent"]
la_master["use_welsh_percent"] = la_master[welsh_cols].sum(axis=1)
la_master.drop(columns=welsh_cols, inplace=True)

# Create summary ethnicity columns by summing groups
la_master["eth_white_percent"] = la_master.filter(regex=("^White")).sum(axis=1)
la_master["eth_asian_percent"] = la_master.filter(regex=("^Asian")).sum(axis=1)
la_master["eth_black_percent"] = la_master.filter(regex=("^Black")).sum(axis=1)
la_master["eth_mixed_percent"] = la_master.filter(regex=("^Mixed")).sum(axis=1)
la_master["eth_other_percent"] = la_master.filter(regex=("^Other")).sum(axis=1)

ethnicity_cols = la_master.filter(regex=("^White|^Asian|^Black|^Mixed|^Other")).columns
la_master.drop(columns=ethnicity_cols, inplace=True)


# IMD
imd_cols = la_master.filter(regex=("LSOAs")).columns
# What percentage of LSOAs in this LA are from the top 20% most deprived in Wales?
la_master["wimd_20pct_percent"] = (
    la_master[imd_cols[2]] / la_master[imd_cols[0]]
) * 100
la_master.drop(columns=imd_cols, inplace=True)


# Vulnerable - just keep percentage for now.
la_master.drop(columns="vulnerable_count", inplace=True)


# For now, just keep the percentage of people who feel they belong in their local area
belonging_cols = la_master.filter(regex=("belong")).columns
la_master["belong_percent"] = (
    la_master["belong_agree_pct"] + la_master["belong_strongagree_pct"]
)
la_master.drop(columns=belonging_cols, inplace=True)


# Write out to csv
la_master.to_csv("cleaned/master_static_LA.csv")
