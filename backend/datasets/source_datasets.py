"""Handles reading of datasets from static/source folder"""

import os
from functools import partial

from .dataset import SourceDataset, DataResolution, UnsupportedDataResolution
from transforms import Transpose, IndexLocSelector, ResetIndex, Compose
from transforms import Rename, Drop
from datasets import SOURCE_DATA_FOLDER

# Shortcut to join Base Data folder with data file names
p = partial(os.path.join, SOURCE_DATA_FOLDER)


# Utils
# -----
def _validate_resolution(resolution: DataResolution, dataset_name: str = ""):
    """
    Raises
    ------
    ValueError: If provided data resolution is None
    UnsupportedDataResolution: Runtime Error if the resolution specified is
        not LA or LSOA (currently the only two supported data resolutions)
    """
    if resolution is None:
        raise ValueError("Please specify a resolution of interest for data")
    if resolution not in (DataResolution.LSOA, DataResolution.LA):
        raise UnsupportedDataResolution(dataset_name=dataset_name)


# ------------------------------
# Load Source Datasets functions
# ------------------------------
def load_language_source_data(resolution: DataResolution) -> SourceDataset:
    """
    Welsh Language Source Data.
    Data is available at both LA and LSOA resolutions.
    Original source data files:
        - LA: "la_welsh_frequency_2018-19.CSV"
        - LSOA: "lsoa_welsh_language_2011.CSV"

    Parameters
    ----------
    resolution: DataResolution
        Resolution of interest for the dataset.
        Supported resolutions are now LA and LSOA

    Returns
    -------
        SourceDataset: Instance of SourceDataset for Welsh Language Data.

    Raises
    ------
    ValueError: If the resolution specified is None
    UnsupportedData: if the resolution specified is
        not LA or LSOA (currently the only two supported data resolutions)
    """
    try:
        _validate_resolution(resolution, dataset_name="Welsh Language")
    except Exception as e:
        raise e
    else:
        ds_name = "welsh_language"
        if resolution == DataResolution.LSOA:
            sd = SourceDataset(
                filepath=p("lsoa_welsh_language_2011.csv"),
                resolution=resolution,
                name=ds_name,
                usecols=[2, 3],
            )
        else:
            sd = SourceDataset(
                filepath=p("la_welsh_frequency_2018-19.csv"),
                resolution=resolution,
                name=ds_name,
                usecols=[1, 2, 3, 4],
            )
        return sd


def load_population_source_data(
    resolution: DataResolution, over_65: bool = False
) -> SourceDataset:
    """
    Welsh Population Source Data.
    Data is available at both LA and LSOA resolution.
    Moreover, it is possible to filter data by selecting
    only subjects age > 65y
    Original source data files:
        - LA: "la_population_age_2019.CSV"
        - LSOA: "lsoa_population_2018_19[_over_65].CSV"

    Parameters
    ----------
    resolution: DataResolution
        Resolution of interest for the dataset.

    over_65: bool (default False)
        Whether to select only "over_65" population

    Returns
    -------
        SourceDataset: Instance of SourceDataset for Welsh Population data.
    """
    try:
        _validate_resolution(resolution, dataset_name="Welsh Population")
    except Exception as e:
        raise e
    else:
        ds_name = "welsh_population"
        if over_65:
            ds_name += "_over65"
        if resolution == DataResolution.LSOA:
            if over_65:
                data_filename = "lsoa_population_2018_19_over_65.csv"
            else:
                data_filename = "lsoa_population_2018_19.csv"
            sd = SourceDataset(p(data_filename), resolution=resolution, name=ds_name)
        else:
            if over_65:
                columns = [3, 14]
            else:
                columns = [3, 15]
            sd = SourceDataset(
                p("la_population_age_2019.csv"),
                resolution=resolution,
                name=ds_name,
                usecols=columns,
            )
        return sd


def load_deprivation_source_data(resolution: DataResolution) -> SourceDataset:
    """
    Welsh IMD (Deprivation) Source Data.
    Data is available at both LA and LSOA resolution.
    Original source data files:
        - LA: "la_WIMD_2019.csv"
        - LSOA: "lsoa_IMD_2019.CSV"

    Parameters
    ----------
    resolution: DataResolution
        Resolution of interest for the dataset.

    Returns
    -------
        SourceDataset: Instance of SourceDataset for Welsh IMD data.
    """
    try:
        _validate_resolution(resolution, dataset_name="IMD")
    except Exception as e:
        raise e
    else:
        ds_name = "deprivation_data"
        if resolution == DataResolution.LSOA:
            sd = SourceDataset(
                p("lsoa_IMD_2019.csv"), name=ds_name, resolution=resolution
            )
        else:
            sd = SourceDataset(
                p("la_WIMD_2019.csv"), name=ds_name, resolution=resolution
            )
        return sd


def load_population_density_source_data(resolution: DataResolution) -> SourceDataset:
    """
    Welsh Population Density Data, available at both LA and LSOA
    resolution.
    Original source data files:
        - LA: "la_pop_density_2018.CSV"
        - LSOA: "lsoa_pop_density_2018-19.XLSX"

    Parameters
    ----------
    resolution: DataResolution
        Resolution of interest for the dataset.

    Returns
    -------
        SourceDataset: Instance of SourceDataset for Welsh Population Density.
    """
    try:
        _validate_resolution(resolution, dataset_name="Population Density")
    except Exception as e:
        raise e
    else:
        ds_name = "population_density"
        if resolution == DataResolution.LSOA:
            sd = SourceDataset(
                p("lsoa_pop_density_2018-19.xlsx"),
                resolution=resolution,
                name=ds_name,
                sheet_name=3,
                usecols="A,B,E",
                skiprows=4,
            )
        else:
            sd = SourceDataset(
                p("la_pop_density_2018.csv"),
                resolution=resolution,
                name=ds_name,
                usecols=[1, 11],
            )
        return sd


def load_vulnerability_source_data() -> SourceDataset:
    """
    Vulnerability data - ONLY available at LA resolution.
    Original source data file:
        - LA: "la_vulnerableProxy_and_cohesion.XLSX"

    Returns
    -------
        SourceDataset instance encapsulating Vulnerability Data
    """
    ds_name = "vulnerability_data"
    transform = Compose(
        [
            IndexLocSelector(idxloc=[1, 20, 21, 38]),
            Transpose(),
            ResetIndex(),
            IndexLocSelector(cloc=[0, 4]),
        ]
    )
    return SourceDataset(
        filepath=p("la_vulnerableProxy_and_cohesion.xlsx"),
        name=ds_name,
        transform=transform,
        resolution=DataResolution.LA,
        sheet_name="By local authority",
        usecols="B:X",
    )


def load_community_cohesion_source_data() -> SourceDataset:
    """Community Cohesion Data - ONLY available
    for LA resolution.
    Original source data file:
        - LA: "la_vulnerableProxy_and_cohesion.XLSX"

    Returns
    -------
        SourceDataset instance for the Community and Cohesion Data
    """
    ds_name = "community_cohesion_data"
    transform = Compose(
        [
            IndexLocSelector(idxloc=[1, 20, 21, 38]),
            Transpose(),
            ResetIndex(),
            IndexLocSelector(cloc=[0, 2, 3]),
        ]
    )
    return SourceDataset(
        filepath=p("la_vulnerableProxy_and_cohesion.xlsx"),
        name=ds_name,
        transform=transform,
        resolution=DataResolution.LA,
        sheet_name="By local authority",
        usecols="B:X",
    )


def load_internet_access_source_data() -> SourceDataset:
    """Internet Access Source Dataset,
    ONLY available for LA resolution.
    Original source data file:
        - LA: "national_survey_internet_use_and_access_la.XLSX"

    Returns
    -------
        SourceDataset instance for the Internet Access Data.
    """
    ds_name = "internet_access_data"
    return SourceDataset(
        p("national_survey_internet_use_and_access_la.xlsx"),
        resolution=DataResolution.LA,
        name=ds_name,
        usecols="A,B",
        skiprows=4,
        nrows=22,
    )


def load_internet_use_source_data() -> SourceDataset:
    """Frequency of Internet Use Source Dataset,
    ONLY available at LA resolution.
    Original source data file:
        - LA: "national_survey_internet_use_and_access_la.XLSX"

    Returns
    -------
        SourceDataset instance for the Internet Use Data.
    """
    # NB Here we aren't reading in the last column, because it is half empty.
    ds_name = "internet_use_data"
    return SourceDataset(
        p("national_survey_internet_use_and_access_la.xlsx"),
        resolution=DataResolution.LA,
        name=ds_name,
        usecols="A,B,C",
        skiprows=34,
        nrows=22,
    )


def load_ethnicity_source_data() -> SourceDataset:
    """Ethnicity Source Dataset, only available at LA resolution.
    Original source data file:
        - LA: "la_lhb_ethnicity.XLSX"

    Returns
    -------
        SourceDataset instance proxy for Ethnicity Data
    """
    ds_name = "ethnicity_data"
    # This data is formatted the wrong way in the spreadsheet so needs extra work
    transform = Compose(
        [
            Transpose(),
            ResetIndex(drop=False),
            Drop(labels=lambda d: d.columns[1], axis=1),
            Rename(columns={"index": 0}),
            Rename(columns=lambda d: {i: c for i, c in enumerate(d.iloc[0].values)}),
            Drop(labels=lambda d: d.index[0]),
        ]
    )
    return SourceDataset(
        p("la_lhb_ethnicity.xlsx"),
        resolution=DataResolution.LA,
        name=ds_name,
        transform=transform,
        sheet_name="By Local Authority",
        usecols="B:X",
    )


# TODO: Add LA and LSOA (raw) Dataset loading functions and tests!
