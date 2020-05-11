"""Python module to create master datasets of LA and LSOA data"""

import os
import pandas as pd
from functools import reduce
from warnings import warn

# Local imports
import data.standardise_datasets as s

# +++++++++++++++++++++
# Changeable constants
# +++++++++++++++++++++

STATIC_CLEANED_FOLDER = os.path.join(
    os.path.abspath(os.path.dirname("__file__")), "data", "static", "cleaned"
)
LIVE_CLEANED_FOLDER = os.path.join(
    os.path.abspath(os.path.dirname("__file__")), "data", "live", "cleaned"
)
LIVE_TRANSFORMED_FOLDER = os.path.join(
    os.path.abspath(os.path.dirname("__file__")), "data", "live", "transformed"
)

# list of files from standardised_datasets
LSOA_STATIC_DATASETS = [
    s.LSOA_WELSH,
    s.LSOA_POPULATION,
    s.LSOA_OVER_65,
    s.LSOA_POPDENSITY,
]

LA_STATIC_DATASETS = [
    s.LA_WELSH,
    s.LA_POPULATION,
    s.LA_OVER_65,
    s.LA_IMD,
    s.LA_VULNERABLE,
    s.LA_COHESION,
    s.LA_INTERNET_ACCESS,
]

LA_LIVE_DATASETS = [
    os.path.join(LIVE_CLEANED_FOLDER, "phwCovidStatement.csv"),
    # os.path.join(LIVE_TRANSFORMED_FOLDER, 'groupCount.csv')
]

# +++++++++++++++++++++++++++++++
# Funcs to generate master files
# +++++++++++++++++++++++++++++++


def generate_la_master():
    """Apply series of functions to create valid la master file"""

    # Marge dataframe of all LA files in /cleaned
    la_master = merge_LA_files(LA_STATIC_DATASETS, LA_LIVE_DATASETS)

    # Apply some final pruning and collation of variables
    la_master = create_daily_internet_col(la_master)
    la_master = create_welsh_col(la_master)
    la_master = create_summary_ethnicity_cols(la_master)
    la_master = create_wimd_col(la_master)
    drop_vulnerable_count(la_master)

    return la_master


def generate_lsoa_master():
    """Apply series of functions to create valid lsoa master file"""

    # Marge dataframe of all LSOA files in /cleaned
    lsoa_master = merge_LSOA_files(LSOA_STATIC_DATASETS)

    # Apply some final pruning and collation of variables
    lsoa_master = create_over_65_col(lsoa_master)

    return lsoa_master


# ++++++++++++++++++++
# Create master files
# ++++++++++++++++++++

LA_MASTER = generate_la_master()
LSOA_MASTER = generate_lsoa_master()


# ++++++++++++++++
# Merge functions
# ++++++++++++++++


def merge_LSOA_files(lsoa_static_datasets):
    # Call .standardise() on each dataset
    static_datasets = map(lambda d: d.standardise(), lsoa_static_datasets)
    static_datasets = map(lambda d: d.standardised_data(), static_datasets)
    static_datasets = map(
        lambda d: d.set_index(["LSOA11CD", "LSOA11NM"]), static_datasets
    )

    static_data = reduce(
        lambda left, right: pd.merge(left, right, left_index=True, right_index=True),
        static_datasets,
    )

    static_data.rename(
        index={"lad19cd": "area_code", "lad19nm": "area_name"}, inplace=True
    )

    # Check that this has worked
    if static_data.shape[0] != 1909:
        raise Exception(
            "An error has occured. There are not the expected 22 rows in the LA dataset."
        )

    return static_data


def merge_LA_files(la_static_datasets, la_live_datasets):

    # Call .standardise() on each dataset
    static_datasets = map(lambda d: d.standardise(), la_static_datasets)
    static_datasets = map(lambda d: d.standardised_data(), static_datasets)
    static_datasets = map(
        lambda d: d.set_index(["lad19cd", "lad19nm"]), static_datasets
    )

    # Read the live datasets to a dictionary, then make a list of the dataframes
    d = {}
    for filepath in la_live_datasets:
        d[os.path.basename(filepath)]: pd.read_csv(
            filepath, index_col=["areaID", "la_name"]
        )
    live_datasets = list(d.values())

    # Merge both sets of dataframes on their indexes
    static_data = reduce(
        lambda left, right: pd.merge(left, right, left_index=True, right_index=True),
        static_datasets,
    )

    # Only merge the live datasets if necessary, if only one, set it as live_data
    if len(live_datasets) > 1:
        live_data = reduce(
            lambda left, right: pd.merge(
                left, right, left_index=True, right_index=True
            ),
            live_datasets,
        )
    else:
        live_data = live_datasets[0]

    # Make the index names consistent with frontend requirements
    static_data.rename(
        index={"lad19cd": "area_code", "lad19nm": "area_name"}, inplace=True
    )
    live_data.rename(
        index={"areaID": "area_code", "la_name": "area_name"}, inplace=True
    )

    # Lastly, merge the two dataframes to create the master dataset for LA
    data = pd.merge(static_data, live_data, on=["area_code"])

    # Check that this has worked
    if data.shape[0] != 22:
        raise Exception(
            "An error has occured. There are not the expected 22 rows in the LA dataset."
        )

    return data


# +++++++++++++++
# LSOA functions
# +++++++++++++++


def create_over_65_col(lsoa_master: pd.DataFrame):
    """Create a new over_65 column in the LSOA master and drop the redundant columns.
    """
    # Crate new 'over 65' variable for the population data (adding up all
    # singlar age cols from 65:90+)
    age_cols = lsoa_master.columns[
        pd.to_numeric(lsoa_master.columns, errors="coerce").to_series().notnull()
    ]
    lsoa_master["over_65_count"] = (
        lsoa_master[age_cols].sum(axis=1) + lsoa_master["90+"]
    )
    lsoa_master.drop(columns=age_cols, inplace=True)
    lsoa_master.drop(columns="90+", inplace=True)
    return lsoa_master


# +++++++++++++
# LA functions
# +++++++++++++


def create_daily_internet_col(la_master: pd.DataFrame):
    """Sum daily internet use columns to create summary col, and drop redundant columns.
    """
    # Get the sum of the people who use the internet daily
    internet_use_cols = ["use_daily_percent", "use_several_daily_percent"]
    la_master["use_internet_daily_percent"] = la_master[internet_use_cols].sum(axis=1)
    la_master.drop(columns=internet_use_cols, inplace=True)
    return la_master


def create_welsh_col(la_master: pd.DataFrame):
    """Sums welsh speaking frequency to create overall welsh speaking column, and drop redundant columns.
    """
    # Get the sum of the people who do use Welsh at all
    welsh_cols = [
        "welsh_daily_percent",
        "welsh_weekly_percent",
        "welsh_lessoften_percent",
    ]
    la_master["welsh_speakers_percent"] = la_master[welsh_cols].sum(axis=1)
    la_master.drop(columns=welsh_cols, inplace=True)
    return la_master


def create_summary_ethnicity_cols(la_master: pd.DataFrame):
    """Sum ethnicity percentages by top level group, and drop redundant columns."""

    # Create summary ethnicity columns by summing groups
    la_master["eth_white_percent"] = la_master.filter(regex=("^White")).sum(axis=1)
    la_master["eth_asian_percent"] = la_master.filter(regex=("^Asian")).sum(axis=1)
    la_master["eth_black_percent"] = la_master.filter(regex=("^Black")).sum(axis=1)
    la_master["eth_mixed_percent"] = la_master.filter(regex=("^Mixed")).sum(axis=1)
    la_master["eth_other_percent"] = la_master.filter(regex=("^Other")).sum(axis=1)

    # Drop redundant columns
    ethnicity_cols = la_master.filter(
        regex=("^White|^Asian|^Black|^Mixed|^Other")
    ).columns
    la_master.drop(columns=ethnicity_cols, inplace=True)

    return la_master


def create_wimd_col(la_master: pd.DataFrame):
    """Generate a column for IMD and drop redundant columns.
    """
    imd_cols = la_master.filter(regex=("LSOAs")).columns
    # What percentage of LSOAs in this LA are from the top 20% most deprived in Wales?
    la_master["wimd_2019"] = (la_master[imd_cols[2]] / la_master[imd_cols[0]]) * 100
    la_master.drop(columns=imd_cols, inplace=True)

    return la_master


def drop_vulnerable_count(la_master: pd.DataFrame):
    """Drop the vulnerable count colulm, in favour of the percentage column"""
    # Vulnerable - just keep percentage for now.
    la_master.drop(columns="vulnerable_count", inplace=True)


def create_belonging_col(la_master: pd.DataFrame):
    """Sum percentages for feelings of belonging, to create summary col. Drop redundant cols"""
    # For now, just keep the percentage of people who feel they belong in
    # their local area
    belonging_cols = la_master.filter(regex=("belong")).columns
    la_master["belong_percent"] = (
        la_master["belong_agree_pct"] + la_master["belong_strongagree_pct"]
    )
    la_master.drop(columns=belonging_cols, inplace=True)

    return la_master
