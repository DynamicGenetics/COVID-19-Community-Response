""""""
import os
from enum import Enum, IntEnum
import geopandas as gpd
import pandas as pd
from typing import Callable

Transform = Callable[[pd.DataFrame], pd.DataFrame]


__all__ = [
    "UnsupportedDataResolution",
    "SourceDataset",
    "DataFormats",
    "DataResolution",
]


#  Exceptions
#  ==========
class UnsupportedDataResolution(RuntimeError):
    def __init__(self, dataset_name: str = None, *args, **kwargs):
        super(UnsupportedDataResolution, self).__init__(*args, **kwargs)
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
    GROUP = 3


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
