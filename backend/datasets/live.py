"""Handles live data from reading to master dataset generation.

This module reads, standardises and defines the master dataset for data sources
from the data/live folder.

Notes
-----
This module imports classes from the `dataset` module.
The `LA_LIVE` master dataset definition has `from_csv=False`. This means that the
live dataset master will always be regenerated from the source files given here,
rather than read from the existing master csv.

To add a new live datasource, follow the existing examples for a `SOURCE_` constant
that is read from file, passed to a `Dataset` definition, and then the Dataset
definition defined in the `LA_LIVE` datasets list to ensure it is included.

"""

import pandas as pd
import os
from functools import partial

from datasets import LIVE_DATA_FOLDER

from datasets.dataset import DataResolution, DataFrequency, Dataset, MasterDataset

p_live = partial(os.path.join, LIVE_DATA_FOLDER)

SOURCE_COVID_COUNT_LA = pd.read_csv(p_live("phwCovidStatement.csv"))

SOURCE_GROUP_COUNTS_LA = pd.read_csv(p_live("groupCount_LA.csv"))

SOURCE_WCVA_ONLINE_LA = pd.read_csv(p_live("la_wcva_2020-05-18.csv"), usecols=[0, 1, 2])

SOURCE_TWEETS_LA = pd.read_csv(p_live("community_tweets.csv"))

SOURCE_ZOE_SUPPORT_LA = pd.read_csv(p_live("help_need20200531.csv"), nrows=3).T
SOURCE_ZOE_SUPPORT_LA.reset_index(level=0, inplace=True)

LA_COVID = Dataset(
    data=SOURCE_COVID_COUNT_LA,
    res=DataResolution.LA,
    key_col="la_name",
    key_is_code=False,
    csv_name="covid_count",
    keep_cols=["lad19nm", "covidIncidence_100k"],
)

LA_GROUP_COUNTS = Dataset(
    data=SOURCE_GROUP_COUNTS_LA,
    res=DataResolution.LA,
    key_col="area_code",
    key_is_code=True,
    rename={"groupCount": "groups_count"},
    csv_name="group_counts",
)

LA_WCVA = Dataset(
    data=SOURCE_WCVA_ONLINE_LA,
    res=DataResolution.LA,
    key_col="AREA",
    key_is_code=False,
    csv_name="wcva_count",
)

LA_TWEETS = Dataset(
    data=SOURCE_TWEETS_LA,
    res=DataResolution.LA,
    key_col="lad19cd",
    key_is_code=True,
    csv_name="tweets_percentage",
)

LA_ZOE_SUPPORT = Dataset(
    data=SOURCE_ZOE_SUPPORT_LA,
    res=DataResolution.LA,
    key_col="index",
    key_is_code=False,
    rename={2: "has_someone_close"},
    keep_cols=["lad19nm", "has_someone_close"],
    bracketed_data_cols=["has_someone_close"],
    csv_name="zoe_support",
)

LA_LIVE = MasterDataset(
    datasets=[LA_COVID, LA_GROUP_COUNTS, LA_WCVA, LA_TWEETS, LA_ZOE_SUPPORT],
    res=DataResolution.LA,
    freq=DataFrequency.LIVE,
    from_csv=False,
)
