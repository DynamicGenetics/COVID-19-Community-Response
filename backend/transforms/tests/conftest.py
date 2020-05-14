import pytest
import pandas as pd
import numpy as np


@pytest.fixture(scope="function")
def dataframe():
    return pd.DataFrame({"A": range(100), "B": range(100, 200), "C": range(200, 300)})


@pytest.fixture(scope="function")
def df_rename_example():
    return pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})


@pytest.fixture(scope="function")
def df_drop_example():
    return pd.DataFrame(np.arange(12).reshape(3, 4), columns=["A", "B", "C", "D"])
