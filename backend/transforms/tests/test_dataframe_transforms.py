import pytest
from pandas.testing import assert_frame_equal
from transforms import Transpose, IndexLocSelector, ResetIndex
from transforms import DataFrameTransformError


def test_transpose_transformation(dataframe):
    t = Transpose()
    assert_frame_equal(t(dataframe), dataframe.T)


def test_iloc_selection_transformation(dataframe):
    t = IndexLocSelector(idxloc=[1, 20, 21, 38])
    assert_frame_equal(t(dataframe), dataframe.iloc[[1, 20, 21, 38]])


def test_iloc_transformation_returns_copy(dataframe):
    t = IndexLocSelector(idxloc=[1])
    assert t(dataframe) is not dataframe.iloc[[1]]
    assert id(t(dataframe)) != id(dataframe.iloc[[1]])


def test_iloc_selection_columns_transformation(dataframe):
    t = IndexLocSelector(cloc=[2])
    assert_frame_equal(t(dataframe), dataframe.iloc[:, [2]])


def test_iloc_selection_rows_and_columns_transformation(dataframe):
    t = IndexLocSelector(idxloc=[3, 4, 23], cloc=[1])
    assert_frame_equal(t(dataframe), dataframe.iloc[[3, 4, 23], [1]])


def test_iloc_selection_transformation_out_of_bounds(dataframe):
    with pytest.raises(DataFrameTransformError):
        t = IndexLocSelector(idxloc=[101])
        t(dataframe)


def test_reset_index_transformation(dataframe):
    with pytest.raises(AssertionError):
        ri = ResetIndex()
        assert_frame_equal(ri(dataframe), dataframe)
