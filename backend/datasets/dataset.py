""""""
import os
from enum import Enum, IntEnum
import geopandas as gpd
import pandas as pd
from typing import Callable

Transform = Callable[[pd.DataFrame], pd.DataFrame]


__all__ = [
    "UnsupportedDataResolution",
    "DataFormats",
    "DataResolution",
]


#  Exceptions
#  ==========
class UnsupportedDataResolution(RuntimeError):
    def __init__(self, dataset_name: str = None, *args):
        super(UnsupportedDataResolution, self).__init__(*args)
        if dataset_name:
            self._ds_name = dataset_name
        else:
            self._ds_name = ""

    def __str__(self):
        s = "Unsupported Data Resolution"
        if self._ds_name:
            s += f" for {self._ds_name}"
        return s


#  =======================
#  Enumeration Definitions
#  =======================
class DataResolution(IntEnum):
    UKN = 0  # Dummy Resolution
    LA = 1
    LSOA = 2
    GROUP = 3  # ready for potential future resolution


DATA_RESOLUTION_KEYS = {
    DataResolution.LA: {"name": "lad19nm", "code": "lad19cd"},
    DataResolution.LSOA: {"name": "LSOA11NM", "code": "LSOA11CD"},
}


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
    name: str (default None)
        If specified, represents a descriptive synthetic name for the dataset.
        By default, the name of the input file will be used.
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
        name: str = None,
        data_format: DataFormats = None,
        transform: Transform = None,
        **read_fn_params,
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
        if name:
            self._name = name
        else:
            fname = os.path.basename(filepath)
            fname, _ = os.path.splitext(fname)
            self._name = fname.strip().replace(" ", "_").lower()
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

    @property
    def name(self):
        res = str(self._resolution).split(".")[1].upper()
        return f"{self._name}_{res}"


# TODO: (old) clean_keys to be executed by default - internally!
# as part of the default preprocessing (e.g. def _preprocess())
# LA and LSOA as instance of Dataset, with corresponding source dataset
# NOT preprocessed!


class Dataset:
    """
    This class encapsulate the logic of a Dataset, as returned by
    (public) methods exposed in the datasets package.

    This class is initialised by a SourceDataset instance of reference.
    Underlying data will be then _standardised_ in order to generate a
    uniform and shared structure, which is independent from the specific
    SourceDataset of reference.
    This new layer around data - separated from SourceDataset - brings
    two main advantages:
        = Keep the original Source Data untouched, for future further / different
        processing;
        = Allow for easy merging and combination/concatenation of Datasets
        (given the shared standardised structure).

    Parameters
    ----------


    """

    def __init__(self, source: SourceDataset, transform: Transform = None):
        self._source = source
        self._transform = transform
        self._data = None

    @property
    def is_valid(self):
        """Proxy property"""
        return self._source.is_valid

    @property
    def resolution(self):
        """Proxy property"""
        return self._source.resolution

    @property
    def source_data(self):
        """Proxy property"""
        return self._source.data

    @property
    def data(self):
        if not self.is_valid:
            return None
        if self._data is None:
            try:
                data_ = self._source.data
                if self._transform:
                    data_ = self._transform(data_)
            except Exception as e:
                self._data = None
                raise e
            else:
                self._data = data_
            return self._data


# data: pd.DataFrame
# key_col: str  # Name of the column that has a unique key
# key_is_code: bool  # Is the key column a LA or LSOA code?
# csv_name: str  # Name for the output CSV
# keep_cols: list = None  # List of columns specifically wanted to keep
# bracketed_data_cols: list = None  # List of columns where data is in the format (DATA (PERCENT))
# rename: dict = None  # Dictionary of columns that need renaming Cleaning {'old_name' : 'new_name' }
# std_data_: pd.DataFrame = field(init=False, default=None)


# def csv_path(self):
#     return os.path.join(
#         "cleaned", "{res}_{name}.csv".format(res=self.res, name=self.csv_name)
#     )
# def _merge_key(self):
#
#     if self.res == DataResolution.LA:
#         return "lad19cd"
#     elif self.res == DataResolution.LSOA:
#         return "LSOA11CD"
#     else:
#         raise TypeError("Unsupported Resolution")
#
# def __add__(self, other):
#
#     if not isinstance(other, Dataset):
#         raise TypeError(
#             "unsupported operand type(s) for +: {} and {}", self.__class__, type(other),
#         )
#
#     if not self.is_standardised or not other.is_standardised:
#         raise TypeError(
#             "Unsupported operand: both dataset needs to be "
#             "standardised before merging!"
#         )
#
#     if self.res != other.res:
#         raise TypeError(
#             "Unsupported operand: both dataset needs to be " "at the same resolution!"
#         )
#
#     merge_key = self._merge_key()
#     self.std_data_ = pd.merge(
#         self.std_data_,
#         other.standardised_data,
#         on=merge_key,
#         left_index=True,
#         right_index=True,
#     )
#     return self
