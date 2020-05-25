import pandas as pd
import os
from functools import partial

from datasets import SOURCE_DATA_FOLDER, LIVE_DATA_FOLDER

from datasets.dataset import DataResolution, DataFrequency, Dataset, MasterDataset

p_live = partial(os.path.join, LIVE_DATA_FOLDER)

SOURCE_COVID_COUNT_LA = pd.read_csv(p_live("phwCovidStatement.csv"))

SOURCE_GROUP_COUNTS_LA = pd.read_csv(p_live("groupCount_LA.csv"))

SOURCE_WCVA_ONLINE_LA = pd.read_csv(p_live("la_wcva_2020-05-18.csv"), usecols=[0, 1, 2])


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

LA_LIVE = MasterDataset(
    datasets=[LA_COVID, LA_GROUP_COUNTS, LA_WCVA],
    res=DataResolution.LA,
    freq=DataFrequency.LIVE,
    from_csv=False,
)
