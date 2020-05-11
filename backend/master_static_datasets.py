"""Python module to handle loading variable data"""

import os
import pandas as pd
from functools import reduce
from warnings import warn
from dataclasses import dataclass

DATA_FOLDER = os.path.join(
    os.path.abspath(os.path.dirname("__file__")), "data", "static", "cleaned"
)


@dataclass
class Dataset:
    """(Data)Class encapsulating information for a single
    Dataset. Dataset instances will be saved into
    a global DATA_DICTIONARY (see below) acting as a
    proxy to access available datasets.

    This mechanism acts as a surrogate for a Database
    and so potentially subject to change in the future.
    """

    name: str  # dataset unique name
    data_format: str  # format of the data (e.g. CSV)
    filename: str  # name of the datafile

    @property
    def source_path(self):
        try:  # BTAFTP
            data_path = os.path.join(DATA_FOLDER, self.filename)
            with open(data_path) as _:
                pass
        except FileNotFoundError:
            raise FileNotFoundError(f'Data source for "{self.name}" does not exist.')
        else:
            return data_path

    @property
    def is_valid(self):
        try:
            _ = self.source_path
        except FileNotFoundError:
            return False
        else:
            return True

    @property
    def data(self):
        if self.data_format == "csv":
            return pd.read_csv(self.source_path)
        raise NotImplementedError(f'Data Format for "{self.name}" not yet suported')


# datamap of each variable

DATAMAP = {
    "la_master": Dataset(
        name="Master file of all LA variables",
        data_format="csv",
        filename="master_static_LA.csv",
    ),
    "lsoa_master": Dataset(
        name="Master file of all LSOA variables",
        data_format="csv",
        filename="master_static_LSOA.csv",
    ),
}


def load_la_master() -> Dataset:

    la_master = DATAMAP["la_master"]
    if not la_master.is_valid:
        # generate_la_master()
        print("Datasets need to be generated")
    return la_master
