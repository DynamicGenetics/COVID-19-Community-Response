import pytest
import pandas as pd

from datasets import DataResolution


def test_dataresolution():
    assert DataResolution.LA == "LA"
