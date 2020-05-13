from transforms import Compose
from transforms import Transpose, IndexLocSelector, ResetIndex
from pandas.testing import assert_frame_equal


def test_compose_transform(dataframe):
    # similar pipeline to create vulnerable and cohesion data
    p = Compose(
        transforms=[IndexLocSelector(idxloc=[1, 20, 21, 38]), Transpose(), ResetIndex()]
    )
    assert_frame_equal(p(dataframe), dataframe.iloc[[1, 20, 21, 38]].T.reset_index())


def test_compose_transform_with_repeated_transformation(dataframe):
    # similar pipeline to create Vulnerable LA after vulnerable and cohesion data
    p = Compose(
        transforms=[
            IndexLocSelector(idxloc=[1, 20, 21, 38]),
            Transpose(),
            ResetIndex(),
            IndexLocSelector(cloc=[0, 4]),
        ]
    )
    assert_frame_equal(
        p(dataframe), dataframe.iloc[[1, 20, 21, 38]].T.reset_index().iloc[:, [0, 4]]
    )
