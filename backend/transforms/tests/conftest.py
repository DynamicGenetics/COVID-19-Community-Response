import pytest
import pandas as pd


@pytest.fixture(scope="function")
def dataframe():
    return pd.DataFrame({"A": range(100), "B": range(100, 200), "C": range(200, 300)})
