"""Python module to handle loading master datasets of static variables"""

import os
import pandas as pd
from functools import reduce
from warnings import warn
from dataclasses import dataclass

DATA_FOLDER = os.path.join(
    os.path.abspath(os.path.dirname("__file__")), "data", "static", "cleaned"
)


@dataclass
class Dataset:
    """(Data)Class encapsulating information for a single
    Dataset. Dataset instances will be saved into
    a global DATA_DICTIONARY (see below) acting as a
    proxy to access available datasets.

    This mechanism acts as a surrogate for a Database
    and so potentially subject to change in the future.
    """

    name: str  # dataset unique name
    data_format: str  # format of the data (e.g. CSV)
    filename: str  # name of the datafile

    @property
    def source_path(self):
        try:  # BTAFTP
            data_path = os.path.join(DATA_FOLDER, self.filename)
            with open(data_path) as _:
                pass
        except FileNotFoundError:
            raise FileNotFoundError(f'Data source for "{self.name}" does not exist.')
        else:
            return data_path

    @property
    def is_valid(self):
        try:
            _ = self.source_path
        except FileNotFoundError:
            return False
        else:
            return True

    @property
    def data(self):
        if self.data_format == "csv":
            return pd.read_csv(self.source_path)
        raise NotImplementedError(f'Data Format for "{self.name}" not yet suported')


DATAMAP = {
    "la_master": Dataset(
        name="Master file of all LA variables",
        data_format="csv",
        filename="master_static_LA.csv",
    ),
    "lsoa_master": Dataset(
        name="Master file of all LSOA variables",
        data_format="csv",
        filename="master_static_LSOA.csv",
    ),
}


def load_la_master() -> Dataset:

    la_master = DATAMAP["la_master"]
    if not la_master.is_valid:
        generate_la_master()
    return la_master


def load_lsoa_master() -> Dataset:

    lsoa_master = DATAMAP["lsoa_master"]
    if not lsoa_master.is_valid:
        generate_lsoa_master()
    return lsoa_master


def generate_la_master(data_filename: str = "master_static_LA.csv"):
    """Apply series of functions to create valid la master file"""

    # Marge dataframe of all LA files in /cleaned
    la_master = collect_area_data(filename_prefix="_LA")

    # Apply some final pruning and collation of variables
    la_master = create_daily_internet_col(la_master)
    la_master = create_welsh_col(la_master)
    la_master = create_summary_ethnicity_cols(la_master)
    la_master = create_wimd_col(la_master)
    drop_vulnerable_count(la_master)

    # Write file out
    warn("Local Authority master dataset generated!")
    la_master.to_file(os.path.join(DATA_FOLDER, data_filename), driver="csv")


def generate_lsoa_master(data_filename: str = "master_static_LSOA.csv"):
    """Apply series of functions to create valid lsoa master file"""

    # Marge dataframe of all LSOA files in /cleaned
    lsoa_master = collect_area_data(filename_prefix="_LSOA")

    # Apply some final pruning and collation of variables
    lsoa_master = create_over_65_col(lsoa_master)

    # Write file out
    warn("Local Authority master dataset generated!")
    lsoa_master.to_file(os.path.join(DATA_FOLDER, data_filename), driver="csv")


def collect_area_data(filename_prefix: str, directory="data/static/cleaned"):
    """Collects the files in the directory with assigned prefix and joins them into one dataframe.

    Arguments:
        filename_prefix {str} -- The prefix of the files collected for the master file.

    Returns:
        pd.DataFrame -- A df of all the variables read from the relevant files.
    """
    # Initialise some values for the loop
    varbs = {}
    i = 0

    # Get directory values (using walk cause we just need one level)
    root, dirnames, filenames = next(os.walk(directory))

    # Iterate through relevant files and add them to the dictionary
    for filename in enumerate(filenames):
        if filename.startswith(filename_prefix):
            filepath = os.path.join(root, filename)
            varbs["df{}".format(i)] = pd.read_csv(filepath, index_col=[0, 1])
            i += 1  # Add one to the i constant

    # Make a list of all the dataframes for the merge.
    varb_list = list(varbs.values())

    # Merge all the dataframes on the indexes
    master = reduce(
        lambda left, right: pd.merge(left, right, left_index=True, right_index=True),
        varb_list,
    )

    return master


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
