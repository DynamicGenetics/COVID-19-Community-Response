"""Collection of (DataFrame) Transformers (a-la-PyTorch)
to inject in Datasets to allow for automation in Data Loading

Each Transformers will be a callable accepting a data frame in input
and returning a new (transformed) dataframe in output.
In this way, multiple transformed may be `Composed`
together to create a transformation pipeline.
"""

import pandas as pd
from typing import List, Union
from pandas.core.indexing import IndexingError

__all__ = ["Transpose", "IndexLocSelector", "ResetIndex", "DataFrameTransformError"]


#  Exceptions and Errors
# ----------------------
class DataFrameTransformError(RuntimeError):
    def __init__(self, internal_error, *args):
        super(DataFrameTransformError, self).__init__(*args)
        self.internal_error = internal_error

    def __str__(self):
        return "DataFrameTransformError ==> {}".format(str(self.internal_error))


# Transformers
# ------------
class Transpose:
    """Simply Transpose a DataFrame"""

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.T


class IndexLocSelector:
    """Select via Indexing (iloc) on selected rows and columns.
    A new copy of the selected dataframe is returned to
    allow for further transformations.

    If any IndexError is raised, a new DataFrameTransformError
    is raised, enclosing the IndexError.
    """

    def __init__(
        self,
        idxloc: Union[slice, List[int]] = None,
        cloc: Union[slice, List[int]] = None,
    ):
        self._idxloc = idxloc
        self._cloc = cloc

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            r, c = df.shape
            if self._idxloc is None:
                self._idxloc = slice(0, r)
            if self._cloc is None:
                self._cloc = slice(0, c)
            df_c = df.iloc[self._idxloc, self._cloc]
        except (IndexingError, IndexError) as e:
            raise DataFrameTransformError(internal_error=e)
        else:
            return df_c.copy()


class ResetIndex:
    """Reset the Index of the DataFrame.
    This transformer wraps the current implementation
    of pd.DataFrame.reset_index only for the drop parameter
    to keep the transformer simple.
    Always a new DataFrame (copy) will be returned
    to allow for multiple transformations.
    """

    def __init__(self, drop: bool = False):
        self.drop = drop

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        return df.reset_index(drop=self.drop)
