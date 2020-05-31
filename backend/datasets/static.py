"""Module that generates the cleaned datasets for each variable from raw.

This module standardises and defines the master dataset for data sources
from the data/static folder.

Notes
-----
This module imports classes from the `dataset` module, and source dataset
constants from the `static_source_datasets` module.

To add a new datasource, follow the existing examples for a `SOURCE_` constant
that is passed to a `Dataset` definition, and then add the Dataset
constant to the MasterDataset datasets list to ensure it is included.

The `LSOA_STATIC` and `LA_STATIC` master datasets have `from_csv=True`. This means
that the master datasets will always be read from a previously generated master csv,
rather than regenerated from source files. If new sources are added, this will need
to be run at least once with `from_csv=False` to integrate new sources into a new
master csv.

"""

from datasets.dataset import Dataset, MasterDataset, DataResolution, DataFrequency
import datasets.static_source_datasets as s


LA_SHIELDING = Dataset(
    data=s.SOURCE_SHEILDING_LA,
    res=DataResolution.LA,
    key_col="la_name",
    key_is_code=False,
    csv_name="LA_shielded_pop_count",
)

LSOA_WELSH = Dataset(
    data=s.SOURCE_WELSH_LSOA,
    res=DataResolution.LSOA,
    key_col="Unnamed: 2",
    key_is_code=True,
    csv_name="welsh_speakers_percent",
    rename={"Percentage able to speak Welsh ": "welsh_speakers_percent"},
)

LA_WELSH = Dataset(
    data=s.SOURCE_WELSH_LA,
    res=DataResolution.LA,
    key_col="Unnamed: 1",
    key_is_code=False,
    csv_name="welsh_speakers_percent",
    rename={
        "Daily ": "welsh_daily_percent",
        "Weekly ": "welsh_weekly_percent",
        "Less Often ": "welsh_lessoften_percent",
    },
)

LSOA_POPULATION = Dataset(
    data=s.SOURCE_POPULATION_LSOA,
    res=DataResolution.LSOA,
    key_col="Area Codes",
    key_is_code=True,
    csv_name="population_count",
    rename={"All Ages": "population_count"},
)

LA_POPULATION = Dataset(
    data=s.SOURCE_POPULATION_LA,
    res=DataResolution.LA,
    key_col="Unnamed: 3",
    key_is_code=False,
    csv_name="population_count",
    rename={"All ages .1": "population_count"},
)

LSOA_OVER_65 = Dataset(
    data=s.SOURCE_OVER_65_LSOA,
    res=DataResolution.LSOA,
    key_col="Area Codes",
    key_is_code=True,
    csv_name="over_65_count",
)

LA_OVER_65 = Dataset(
    data=s.SOURCE_OVER_65_LA,
    res=DataResolution.LA,
    key_col="Unnamed: 3",
    key_is_code=False,
    csv_name="over_65_count",
    rename={"Unnamed: 14": "over_65_count"},
)

LSOA_IMD = Dataset(
    data=s.SOURCE_IMD_LSOA,
    res=DataResolution.LSOA,
    key_col="lsoa11cd",
    key_is_code=True,
    csv_name="wimd_2019",
    keep_cols=["LSOA11CD", "wimd_2019"],
)

LA_IMD = Dataset(
    data=s.SOURCE_IMD_LA,
    res=DataResolution.LA,
    key_col="Unnamed: 0",
    key_is_code=False,
    csv_name="wimd_2019",
)

LSOA_POPDENSITY = Dataset(
    data=s.SOURCE_POPDENSITY_LSOA,
    res=DataResolution.LSOA,
    key_col="Code",
    key_is_code=True,
    rename={"People per Sq Km": "pop_density_persqkm"},
    keep_cols=["LSOA11CD", "pop_density_persqkm"],
    csv_name="pop_density_persqkm",
)

LA_POPDENSITY = Dataset(
    data=s.SOURCE_POPDENSITY_LA,
    res=DataResolution.LA,
    key_col="Unnamed: 1",
    key_is_code=False,
    rename={"Mid-year 2018 ": "pop_density_persqkm"},
    csv_name="pop_density_persqkm",
)

LA_VULNERABLE = Dataset(
    data=s.SOURCE_VULNERABLE_LA,
    res=DataResolution.LA,
    key_col="index",
    key_is_code=False,
    rename={38: "vulnerable"},
    bracketed_data_cols=["vulnerable"],
    csv_name="vulnerable_count_percent",
)

LA_COHESION = Dataset(
    data=s.SOURCE_COMM_COHESION_LA,
    res=DataResolution.LA,
    key_col="index",
    key_is_code=False,
    rename={20: "belong_strongagree", 21: "belong_agree"},
    bracketed_data_cols=["belong_strongagree", "belong_agree"],
    csv_name="comm_cohesion_count_percent",
)

LA_INTERNET_ACCESS = Dataset(
    data=s.SOURCE_INTERNET_ACCESS_LA,
    res=DataResolution.LA,
    key_col="Unnamed: 0",
    key_is_code=False,
    rename={"Yes (%)": "has_internet_percent"},
    csv_name="has_internet_percent",
)

LA_GP = Dataset(
    data=s.SOURCE_GP_ONLINE_LA,
    res=DataResolution.LA,
    key_col="ladcd",
    key_is_code=True,
    keep_cols=["lad19cd", "MHOL_pct"],
    csv_name="gp",
)

# LA_INTERNET_USE = Dataset(
#     data=s.SOURCE_INTERNET_USE_LA,
#     res=DataResolution.LA,
#     key_col="Unnamed: 0",
#     key_is_code=False,
#     rename={
#         "Several times a day (%)": "use_several_daily_percent",
#         "Daily (%) ": "use_daily_percent",
#     },
#     csv_name="use_internet_percent",
# )

# LA_ETHNICITY = Dataset(
#     data=s.SOURCE_ETHNICITY_LA,
#     res=DataResolution.LA,
#     key_col="Unnamed: 1",
#     key_is_code=False,
#     csv_name="ethnicities_percent",
# )


LSOA_STATIC_DATASETS = [
    LSOA_WELSH,
    LSOA_POPULATION,
    LSOA_OVER_65,
    LSOA_POPDENSITY,
    LSOA_IMD,
]

LA_STATIC_DATASETS = [
    LA_SHIELDING,
    LA_WELSH,
    LA_POPULATION,
    LA_OVER_65,
    LA_POPDENSITY,
    LA_IMD,
    LA_VULNERABLE,
    LA_COHESION,
    LA_INTERNET_ACCESS,
    LA_GP,
]

LA_STATIC = MasterDataset(
    datasets=LA_STATIC_DATASETS,
    res=DataResolution.LA,
    freq=DataFrequency.STATIC,
    from_csv=True,
)

LSOA_STATIC = MasterDataset(
    datasets=LSOA_STATIC_DATASETS,
    res=DataResolution.LSOA,
    freq=DataFrequency.STATIC,
    from_csv=True,
)
