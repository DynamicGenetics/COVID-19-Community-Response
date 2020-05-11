import pandas as pd


def create_over_65_col(data: pd.DataFrame):
    """Create a new over_65 column in the LSOA master and drop the redundant columns.
    """
    # Crate new 'over 65' variable for the population data (adding up all
    # singlar age cols from 65:90+)
    age_cols = data.columns[
        pd.to_numeric(data.columns, errors="coerce").to_series().notnull()
    ]
    data["over_65_count"] = data[age_cols].sum(axis=1) + data["90+"]
    data.drop(columns=age_cols, inplace=True)
    data.drop(columns="90+", inplace=True)
    return data


def create_daily_internet_col(data: pd.DataFrame):
    """Sum daily internet use columns to create summary col, and drop redundant columns.
    """
    # Get the sum of the people who use the internet daily
    internet_use_cols = ["use_daily_percent", "use_several_daily_percent"]
    data["use_internet_daily_percent"] = data[internet_use_cols].sum(axis=1)
    data.drop(columns=internet_use_cols, inplace=True)
    return data


def create_welsh_col(data: pd.DataFrame):
    """Sums welsh speaking frequency to create overall welsh speaking column, and drop redundant columns.
    """
    # Get the sum of the people who do use Welsh at all
    welsh_cols = [
        "welsh_daily_percent",
        "welsh_weekly_percent",
        "welsh_lessoften_percent",
    ]
    data["welsh_speakers_percent"] = data[welsh_cols].sum(axis=1)
    data.drop(columns=welsh_cols, inplace=True)
    return data


def create_summary_ethnicity_cols(data: pd.DataFrame):
    """Sum ethnicity percentages by top level group, and drop redundant columns."""

    # Create summary ethnicity columns by summing groups
    data["eth_white_percent"] = data.filter(regex=("^White")).sum(axis=1)
    data["eth_asian_percent"] = data.filter(regex=("^Asian")).sum(axis=1)
    data["eth_black_percent"] = data.filter(regex=("^Black")).sum(axis=1)
    data["eth_mixed_percent"] = data.filter(regex=("^Mixed")).sum(axis=1)
    data["eth_other_percent"] = data.filter(regex=("^Other")).sum(axis=1)

    # Drop redundant columns
    ethnicity_cols = data.filter(regex=("^White|^Asian|^Black|^Mixed|^Other")).columns
    data.drop(columns=ethnicity_cols, inplace=True)

    return data


def create_wimd_col(data: pd.DataFrame):
    """Generate a column for IMD and drop redundant columns.
    """
    imd_cols = data.filter(regex=("LSOAs")).columns
    # What percentage of LSOAs in this LA are from the top 20% most deprived in Wales?
    data["wimd_2019"] = (data[imd_cols[2]] / data[imd_cols[0]]) * 100
    data.drop(columns=imd_cols, inplace=True)

    return data


def drop_vulnerable_count(data: pd.DataFrame):
    """Drop the vulnerable count colulm, in favour of the percentage column"""
    # Vulnerable - just keep percentage for now.
    data.drop(columns="vulnerable_count", inplace=True)


def create_belonging_col(data: pd.DataFrame):
    """Sum percentages for feelings of belonging, to create summary col. Drop redundant cols"""
    # For now, just keep the percentage of people who feel they belong in
    # their local area
    belonging_cols = data.filter(regex=("belong")).columns
    data["belong_percent"] = data["belong_agree_pct"] + data["belong_strongagree_pct"]
    data.drop(columns=belonging_cols, inplace=True)
    return data
