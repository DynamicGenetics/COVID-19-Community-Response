import pytest
from pandas.testing import assert_frame_equal
from transforms import Transpose, IndexLocSelector, ResetIndex
from transforms import Rename, Drop
from transforms import DataFrameTransformError


# Transpose
# =========
def test_transpose_transformation(dataframe):
    t = Transpose()
    assert_frame_equal(t(dataframe), dataframe.T)


# IndexLocSelector
# ================
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


# Reset Index
# ===========
def test_reset_index_transformation(dataframe):
    with pytest.raises(AssertionError):
        ri = ResetIndex()
        assert_frame_equal(ri(dataframe), dataframe)


# Rename
# ======
def test_rename_transformation_index_and_column(df_rename_example):
    r = Rename(index={0: "x", 1: "y", 2: "z"}, columns={"A": "a", "B": "c"})
    assert_frame_equal(
        r(df_rename_example),
        df_rename_example.rename(
            index={0: "x", 1: "y", 2: "z"}, columns={"A": "a", "B": "c"}
        ),
    )


def test_rename_transformation_index_and_column_with_callable(df_rename_example):
    r = Rename(
        index=lambda d: {0: "x", 1: "y", 2: "z"}, columns=lambda d: {"A": "a", "B": "c"}
    )
    assert_frame_equal(
        r(df_rename_example),
        df_rename_example.rename(
            index={0: "x", 1: "y", 2: "z"}, columns={"A": "a", "B": "c"}
        ),
    )


def test_rename_transformation_index_only(df_rename_example):
    r = Rename(index={0: "x", 1: "y", 2: "z"})
    assert_frame_equal(
        r(df_rename_example), df_rename_example.rename(index={0: "x", 1: "y", 2: "z"})
    )


def test_rename_transformation_index_only_with_callable(df_rename_example):
    r = Rename(index=lambda d: {0: "x", 1: "y", 2: "z"})
    assert_frame_equal(
        r(df_rename_example), df_rename_example.rename(index={0: "x", 1: "y", 2: "z"})
    )


def test_rename_transformation_column_only(df_rename_example):
    r = Rename(columns={"A": "a", "B": "c"})
    assert_frame_equal(
        r(df_rename_example), df_rename_example.rename(columns={"A": "a", "B": "c"})
    )


def test_rename_transformation_column_only_with_callable(df_rename_example):
    r = Rename(columns=lambda d: {c: c.lower() for c in d.columns})
    assert_frame_equal(
        r(df_rename_example), df_rename_example.rename(columns={"A": "a", "B": "b"})
    )


def test_rename_transformation_mapper_axis_0(df_rename_example):
    r = Rename(mapper={0: "x", 1: "y", 2: "z"}, axis=0)
    assert_frame_equal(
        r(df_rename_example), df_rename_example.rename(index={0: "x", 1: "y", 2: "z"})
    )


def test_rename_transformation_mapper_axis_0_callable(df_rename_example):
    r = Rename(mapper=lambda d: {0: "x", 1: "y", 2: "z"}, axis=0)
    assert_frame_equal(
        r(df_rename_example), df_rename_example.rename(index={0: "x", 1: "y", 2: "z"})
    )


def test_rename_transformation_mapper_axis_1(df_rename_example):
    r = Rename(mapper={"A": "a", "B": "c"}, axis=1)
    assert_frame_equal(
        r(df_rename_example), df_rename_example.rename(columns={"A": "a", "B": "c"})
    )


def test_rename_transformation_mapper_axis_1_callable(df_rename_example):
    r = Rename(mapper=lambda d: {"A": "a", "B": "c"}, axis=1)
    assert_frame_equal(
        r(df_rename_example), df_rename_example.rename(columns={"A": "a", "B": "c"})
    )


def test_rename_transformation_mapper_wrong_axis(df_rename_example):
    with pytest.raises(DataFrameTransformError):
        r = Rename(mapper={"A": "a", "B": "c"}, axis=3)
        r(df_rename_example)


def test_rename_transformation_mapper_wrong_index_rename(df_rename_example):
    with pytest.raises(DataFrameTransformError):
        r = Rename(mapper={"3": "a", "B": "c"}, axis=0)
        r(df_rename_example)


def test_rename_transformation_mapper_wrong_column_rename(df_rename_example):
    with pytest.raises(DataFrameTransformError):
        r = Rename(mapper={"3": "a", "B": "c"}, axis=1)
        r(df_rename_example)


def test_rename_transformation_callable_exception(df_rename_example):
    with pytest.raises(DataFrameTransformError):
        r = Rename(mapper=lambda d: {"3": "a", "B": "c"}, axis=1)
        r(df_rename_example)


# Drop
# ====
def test_drop_transformation_index_and_column(df_drop_example):
    r = Drop(index=[0], columns=["A", "B"])
    assert_frame_equal(
        r(df_drop_example), df_drop_example.drop(index=[0], columns=["A", "B"])
    )


def test_drop_transformation_index_and_column_with_callables(df_drop_example):
    r = Drop(index=lambda d: [0], columns=lambda d: d.columns[:2])
    assert_frame_equal(
        r(df_drop_example), df_drop_example.drop(index=[0], columns=["A", "B"])
    )


def test_drop_transformation_index_only(df_drop_example):
    r = Drop(index=[0])
    assert_frame_equal(r(df_drop_example), df_drop_example.drop(index=[0]))


def test_drop_transformation_index_only_with_callable(df_drop_example):
    r = Drop(index=lambda d: [0])
    assert_frame_equal(r(df_drop_example), df_drop_example.drop(index=[0]))


def test_drop_transformation_column_only(df_drop_example):
    r = Drop(columns=["A", "B"])
    assert_frame_equal(r(df_drop_example), df_drop_example.drop(columns=["A", "B"]))


def test_drop_transformation_column_only_with_callable(df_drop_example):
    r = Drop(columns=lambda d: ["A", "B"])
    assert_frame_equal(r(df_drop_example), df_drop_example.drop(columns=["A", "B"]))


def test_drop_transformation_labels_axis_0(df_drop_example):
    r = Drop(labels=[0], axis=0)
    assert_frame_equal(r(df_drop_example), df_drop_example.drop(index=[0]))


def test_drop_transformation_labels_on_index_if_axis_not_specified(df_drop_example):
    r = Drop(labels=[0])
    assert_frame_equal(r(df_drop_example), df_drop_example.drop(index=[0]))


def test_drop_transformation_labels_axis_0_with_callable(df_drop_example):
    r = Drop(labels=lambda d: [0], axis=0)
    assert_frame_equal(r(df_drop_example), df_drop_example.drop(index=[0]))


def test_drop_transformation_labels_axis_1(df_drop_example):
    r = Drop(labels=["A", "B"], axis=1)
    assert_frame_equal(r(df_drop_example), df_drop_example.drop(columns=["A", "B"]))


def test_drop_transformation_labels_axis_1_with_callable(df_drop_example):
    r = Drop(labels=lambda d: d.columns[:2], axis=1)
    assert_frame_equal(
        r(df_drop_example), df_drop_example.drop(columns=df_drop_example.columns[:2])
    )


def test_drop_transformation_labels_wrong_axis(df_drop_example):
    with pytest.raises(DataFrameTransformError):
        r = Drop(labels=["A", "B"], axis=3)
        r(df_drop_example)


def test_drop_transformation_labels_wrong_index_drop(df_drop_example):
    with pytest.raises(DataFrameTransformError):
        r = Drop(labels=["A"], axis=0)
        r(df_drop_example)


def test_drop_transformation_labels_wrong_columns_drop(df_drop_example):
    with pytest.raises(DataFrameTransformError):
        r = Drop(labels=["A"], axis=0)
        r(df_drop_example)


def test_drop_transformation_labels_with_failing_callable(df_drop_example):
    with pytest.raises(DataFrameTransformError):
        r = Drop(labels=lambda d: d.columns[0], axis=0)
        r(df_drop_example)


def test_drop_transformation_labels_tuple_type(df_drop_example):
    try:
        r = Drop(labels=("A",), axis=1)
        r(df_drop_example)
        assert True
    except (DataFrameTransformError, Exception):
        assert False
