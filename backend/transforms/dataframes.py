"""Collection of (DataFrame) Transformers (a-la-PyTorch)
to inject in Datasets to allow for automation in Data Loading

Each Transformers will be a callable accepting a data frame in input
and returning a new (transformed) dataframe in output.
In this way, multiple transformed may be `Composed`
together to create a transformation pipeline.
"""

import pandas as pd
from typing import List, Sequence, Union, TypeVar, Callable, Dict
from pandas.core.indexing import IndexingError

T = TypeVar("T", str, int)
Selector = Callable[[pd.DataFrame], Union[pd.Series, Dict]]
DropSelector = Callable[[pd.DataFrame], Union[pd.Series, List[T]]]

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

    def __init__(
        self,
        index: Union[Selector, Dict] = None,
        columns: Union[Selector, Dict] = None,
        mapper: Union[Selector, Dict] = None,
        axis: int = None,
    ):
        self._axis = axis  # No validation of index as pandas doesn't do
        if callable(index):
            self._index_cal = index
            self._index = None
        else:
            self._index_cal = None
            self._index = index

        if callable(columns):
            self._col_call = columns
            self._columns = None
        else:
            self._col_call = None
            self._columns = columns
        if callable(mapper):
            self._mapper_cal = mapper
            self._mapper = None
        else:
            self._mapper_cal = None
            self._mapper = mapper

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            errors = "raise"
            # Check callable first
            if self._index_cal is not None:
                self._index = self._index_cal(df)
            if self._col_call is not None:
                self._columns = self._col_call(df)
            if self._mapper_cal is not None:
                self._mapper = self._mapper_cal(df)

            if self._index is not None or self._columns is not None:
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
        index: Union[DropSelector, str, Sequence[T]] = None,
        columns: Union[DropSelector, str, Sequence[T]] = None,
        labels: Union[DropSelector, str, Sequence[T]] = None,
        axis: int = None,
    ):
        self._axis = 0 if axis is None else axis
        if callable(index):
            self._index_call = index
            self._index = None
        else:
            self._index_call = None
            self._index = index
            if (
                self._index is not None
                and not isinstance(self._index, list)
                and not isinstance(self._index, str)
            ):
                self._index = list(self._index)
        if callable(columns):
            self._columns_call = columns
            self._columns = None
        else:
            self._columns_call = None
            self._columns = columns
            if (
                self._columns is not None
                and not isinstance(self._columns, list)
                and not isinstance(self._columns, str)
            ):
                self._columns = list(self._columns)
        if callable(labels):
            self._labels_call = labels
            self._labels = None
        else:
            self._labels_call = None
            self._labels = labels
            if (
                self._labels is not None
                and not isinstance(self._labels, list)
                and not isinstance(self._labels, str)
            ):
                self._labels = list(self._labels)

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            errors = "raise"
            # Check callable first
            if self._index_call is not None:
                self._index = self._index_call(df)
            if self._columns_call is not None:
                self._columns = self._columns_call(df)
            if self._labels_call is not None:
                self._labels = self._labels_call(df)

            if self._index or self._columns:
                df = df.drop(index=self._index, columns=self._columns, errors=errors)
            else:
                df = df.drop(labels=self._labels, axis=self._axis, errors=errors)
        except (KeyError, ValueError) as e:
            raise DataFrameTransformError(internal_error=e)
        else:
            return df


class FilterOnColumnPrefix:
    """
    Transformer that select a subset filtered input
    dataframe based on the prefix in the name of target
    column. By default, NaN values are removed.
    """

    def __init__(self, column: str, name_contains: str, strip_na: bool = True):
        self._column = column
        self._colname_filter = name_contains
        self._na = ~strip_na

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            df = df[
                df[self._column].str.contains(self._colname_filter, na=self._na)
            ].copy()
        except (ValueError, KeyError) as e:
            raise DataFrameTransformError(internal_error=e)
        else:
            return df


class DropNa:
    """"""

    def __init__(self, columns: Union[str, List[str]]):
        self._subset = columns

    def __call__(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            df = df.dropna(subset=self._subset)
        except (ValueError, KeyError) as e:
            raise DataFrameTransformError(internal_error=e)
        else:
            return df


# TODO: Bracketed Data --> Lambda Transformer with Partial
