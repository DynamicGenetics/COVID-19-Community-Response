"""Handles reading of datasets from source folder"""

import os
from functools import partial

from .dataset import SourceDataset, DataResolution, UnsupportedDataResolution
from transforms import Transpose, IndexLocSelector, ResetIndex, Compose
from transforms import Rename, Drop
from datasets import SOURCE_DATA_FOLDER

# Shortcut to join Base Data folder with data file names
p = partial(os.path.join, SOURCE_DATA_FOLDER)


# ------------------------------
# Load Static Datasets functions
# ------------------------------


# Utils
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


def load_language_data(resolution: DataResolution) -> SourceDataset:
    """
    Welsh Language Data

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
        if resolution == DataResolution.LSOA:
            sd = SourceDataset(
                filepath=p("lsoa_welsh_language_2011.csv"),
                resolution=resolution,
                usecols=[2, 3],
            )
        else:
            sd = SourceDataset(
                filepath=p("la_welsh_frequency_2018-19.csv"),
                resolution=resolution,
                usecols=[1, 2, 3, 4],
            )
        return sd


def load_population_data(
    resolution: DataResolution, over_65: bool = False
) -> SourceDataset:
    """
    Welsh Population Data

    Parameters
    ----------
    resolution: DataResolution
        Resolution of interest for the dataset.
        Supported resolutions are now LA and LSOA

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
        if resolution == DataResolution.LSOA:
            if over_65:
                data_filename = "lsoa_population_2018_19_over_65.csv"
            else:
                data_filename = "lsoa_population_2018_19.csv"
            sd = SourceDataset(p(data_filename), resolution=resolution)
        else:
            if over_65:
                columns = [3, 14]
            else:
                columns = [3, 15]
            sd = SourceDataset(
                p("la_population_age_2019.csv"), resolution=resolution, usecols=columns
            )
        return sd


def load_deprivation_data(resolution: DataResolution) -> SourceDataset:
    """
    Welsh IMD (Deprivation)

    Parameters
    ----------
    resolution: DataResolution
        Resolution of interest for the dataset.
        Supported resolutions are now LA and LSOA

    Returns
    -------
        SourceDataset: Instance of SourceDataset for Welsh IMD data.
    """
    try:
        _validate_resolution(resolution, dataset_name="IMD")
    except Exception as e:
        raise e
    else:
        if resolution == DataResolution.LSOA:
            sd = SourceDataset(p("lsoa_IMD_2019.csv"), resolution=resolution)
        else:
            sd = SourceDataset(p("la_WIMD_2019.csv"), resolution=resolution)
        return sd


def load_population_density_data(resolution: DataResolution) -> SourceDataset:
    """
    Welsh Population Density Data

    Parameters
    ----------
    resolution: DataResolution
        Resolution of interest for the dataset.
        Supported resolutions are now LA and LSOA

    Returns
    -------
        SourceDataset: Instance of SourceDataset for Welsh Population Density.
    """
    try:
        _validate_resolution(resolution, dataset_name="Population Density")
    except Exception as e:
        raise e
    else:
        if resolution == DataResolution.LSOA:
            sd = SourceDataset(
                p("lsoa_pop_density_2018-19.xlsx"),
                resolution=resolution,
                sheet_name=3,
                usecols="A,B,E",
                skiprows=4,
            )
        else:
            sd = SourceDataset(
                p("la_pop_density_2018.csv"), resolution=resolution, usecols=[1, 11]
            )
        return sd


def load_vulnerability_data() -> SourceDataset:
    """Vulnerability data (LA only)"""
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
        transform=transform,
        resolution=DataResolution.LA,
        sheet_name="By local authority",
        usecols="B:X",
    )


def load_community_cohesion_data() -> SourceDataset:
    """Community Cohesion Data (LA only)"""
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
        transform=transform,
        resolution=DataResolution.LA,
        sheet_name="By local authority",
        usecols="B:X",
    )


def load_internet_access_data() -> SourceDataset:
    """Internet Access (LA only)"""
    return SourceDataset(
        p("national_survey_internet_use_and_access_la.xlsx"),
        resolution=DataResolution.LA,
        usecols="A,B",
        skiprows=4,
        nrows=22,
    )


def load_internet_use_data() -> SourceDataset:
    """Internet Access (LA only)"""
    # NB Here we aren't reading in the last column, because it is half empty.
    return SourceDataset(
        p("national_survey_internet_use_and_access_la.xlsx"),
        resolution=DataResolution.LA,
        usecols="A,B,C",
        skiprows=34,
        nrows=22,
    )


def load_ethnicity_data() -> SourceDataset:
    """Ethnicity Data (LA only)"""
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
        transform=transform,
        sheet_name="By Local Authority",
        usecols="B:X",
    )
