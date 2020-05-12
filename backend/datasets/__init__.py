import os
from enum import IntEnum

BASE_FOLDER = os.path.abspath(os.path.dirname(__file__))
SOURCE_DATA_FOLDER = os.path.join(BASE_FOLDER, "data", "static", "source")
GEO_DATA_FOLDER = os.path.join(BASE_FOLDER, "data", "static", "geoboundaries")


class DataResolution(IntEnum):
    UKN = 0  # Dummy Resolution
    LA = 1
    LSOA = 2
    GROUP = 3


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
