"""Handles reading of datasets from source folder"""

import pandas as pd
import geopandas as gpd
import os
from functools import partial
from enum import Enum
from typing import Callable
from transforms import Transpose, IndexLocSelector, ResetIndex, Compose
from transforms import Rename, Drop
from datasets import SOURCE_DATA_FOLDER, UnsupportedDataResolution
from datasets import DataResolution

Transform = Callable[[pd.DataFrame], pd.DataFrame]

# Shortcut to join Base Data folder with data file names
p = partial(os.path.join, SOURCE_DATA_FOLDER)


class DataFormats(Enum):
    CSV = pd.read_csv
    XLS = pd.read_excel
    JSON = pd.read_json
    GEOJSON = gpd.read_file
    UNKNOWN = None


FORMAT_EXTENSIONS = {
    ".csv": DataFormats.CSV,
    ".xls": DataFormats.XLS,
    ".xlsx": DataFormats.XLS,
    ".json": DataFormats.JSON,
    ".geojson": DataFormats.GEOJSON,
}


class SourceDataset:
    """This class encapsulate the logic of a Source (static) Dataset
    as generated from a local data file.
    Supported formats for data files are: CSV, Excel, JSON,
    GeoJSon (using GeoPandas).

    Internal data representation is build on `pandas.DataFrame`
    (`geopandas.GeoDataFrame` for geojson files).

    Data is loaded
    (1) in a lazy fashion, deferring the actual loading of
        data files when it is required,
    (2) just once, so saving and re-using the reference to the data
        for future calls.

    The format of the data to load will be automatically inferred from the
    file name. However, it is possible to specify which is the format
    of the data file - so to force specific loading functions, regardless
    of the used file extensions.

    To allow for lazy deferred loading, extra options to pass to
    the (pandas/geopandas) data loading functions are supported.

    Each SourceDataset is characterised by a resolution property,
    specifying the level of details and geography allowed for
    specific data.

    Finally, it is also possible to inject custom pre-processing
    transformation operations to be automatically applied before
    the actual data is returned.

    Parameters
    ----------
    filepath: str
        Path to the data file
    resolution: DataResolution
        Resolution associated to the Dataset
    data_format: DataFormats (default None)
        Instance of DataFormats enumeration to force a specific
        format and so loading function to use
    transform: Transform (default None)
        Callable instance to apply transformation to data
    read_fn_params:
        Additional parameters to pass to the load function

    Examples
    --------
    >>> d = SourceDataset(filepath='path/to/datafile.csv', resolution=DataResolution.LA)
    >>> d.data_format
    CSV
    >>> d.resolution
    DataResolution.LA
    # This will load a dataset from a CSV file, passing `use_cols=[1, 2]` to
    # underneath pd.read_csv loading function
    >>> d = SourceDataset(filepath='path/to/datafile.csv',
    ...                   resolution=DataResolution.LSOA, use_cols=[1, 2])
    >>> print(d.data.head())
    """

    def __init__(
        self,
        filepath: str,
        resolution: DataResolution,
        data_format: DataFormats = None,
        transform: Transform = None,
        **read_fn_params
    ):
        self._filepath = filepath
        if data_format is None:
            self._read_fn, self._extension = self._infer_format(filepath)
        else:
            self._read_fn = data_format
            reverse_formats_map = {v: k for k, v in FORMAT_EXTENSIONS.items()}
            self._extension = reverse_formats_map[data_format][1:]
        self._read_fn_params = read_fn_params
        self.transform = transform
        self._resolution = resolution
        self._data = None  # Lazy loading

    @staticmethod
    def _infer_format(filepath):
        _, ext = os.path.splitext(filepath)  # this includes '.'
        try:
            fmt = FORMAT_EXTENSIONS[ext]
        except KeyError:
            fmt = DataFormats.UNKNOWN
        return fmt, ext[1:]  # get rid of '.' for extension

    @property
    def is_valid(self):
        return os.path.exists(self._filepath)

    @property
    def data(self):
        if not self.is_valid:
            return None
        if self._data is None:
            try:
                data = self._read_fn(self._filepath, **self._read_fn_params)
                if self.transform:
                    data = self.transform(data)
            except Exception as e:
                self._data = None
                raise e
            else:
                self._data = data
        return self._data

    @property
    def data_format(self):
        return self._extension.upper()

    @property
    def resolution(self):
        return self._resolution


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
