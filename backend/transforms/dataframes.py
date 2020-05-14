"""Collection of (DataFrame) Transformers (a-la-PyTorch)
to inject in Datasets to allow for automation in Data Loading

Each Transformers will be a callable accepting a data frame in input
and returning a new (transformed) dataframe in output.
In this way, multiple transformed may be `Composed`
together to create a transformation pipeline.
"""

import pandas as pd
from typing import List, Sequence, Union, TypeVar
from pandas.core.indexing import IndexingError

T = TypeVar("T", str, int)


__all__ = [
    "Transpose",
    "IndexLocSelector",
    "ResetIndex",
    "Rename",
    "Drop",
    "DataFrameTransformError",
]


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


class Rename:
    """Alter label on specified axis of a Pandas DataFrame.
    This transformer wraps the DataFrame.rename method,
    with the only difference that the inplace parameter is
    not allowed to return a copy of a new dataframe.
    Accepted Parameters:
    - index: mapper for index (mapper, axis=0)
    - columns: mapper for columns (mapper, axis=1)
    - mapper: general mapper (expects axis)
    - axis: axis on which to apply the transformation
    NOTE: The `errors` constant is forced to be "raise" to not
    have a transformation that fails silently
    """

    def __init__(self, index=None, columns=None, mapper=None, axis: int = None):
        self._index = {} if index is None else index
        self._columns = {} if columns is None else columns
        self._axis = axis  # No validation of index as pandas doesn't do
        self._mapper = mapper

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            errors = "raise"
            if self._index or self._columns:
                df = df.rename(index=self._index, columns=self._columns, errors=errors)
            else:
                df = df.rename(mapper=self._mapper, axis=self._axis, errors=errors)
        except (KeyError, ValueError) as e:
            raise DataFrameTransformError(internal_error=e)
        else:
            return df


class Drop:
    """Drop labels on either rows (index) or columns (cols).
    This transformers builds around DataFrame.drop method.
    Accepted parameters:
    - labels: single label or list like
    - axis: axis on which to apply transformation
    - index: labels to drop on index (axis=0)
    - columns: labels to drop on column (axis=1)
    NOTE: errors is forced to be "raise" to not have a pipeline that fails
    silently
    """

    def __init__(
        self,
        index: Union[str, Sequence[T]] = None,
        columns: Union[str, Sequence[T]] = None,
        labels: Union[str, Sequence[T]] = None,
        axis: int = None,
    ):
        self._index = [] if index is None else index
        self._columns = [] if columns is None else columns
        self._axis = axis
        self._labels = [] if labels is None else labels
        if not isinstance(self._index, list) and not isinstance(self._index, str):
            self._index = list(self._index)
        if not isinstance(self._columns, list) and not isinstance(self._columns, str):
            self._columns = list(self._columns)
        if not isinstance(self._labels, list) and not isinstance(self._labels, str):
            self._labels = list(self._labels)

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            errors = "raise"
            if self._index or self._columns:
                df = df.drop(index=self._index, columns=self._columns, errors=errors)
            else:
                df = df.drop(labels=self._labels, axis=self._axis, errors=errors)
        except (KeyError, ValueError) as e:
            raise DataFrameTransformError(internal_error=e)
        else:
            return df
