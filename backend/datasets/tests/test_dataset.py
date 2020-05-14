import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from datasets import SourceDataset, DataResolution

# -----------------------------
# Tests: SourceDataset creation
# -----------------------------


def test_dataset_csv_no_extra_parameter(sample_csv_filepath):
    sd = SourceDataset(sample_csv_filepath, resolution=DataResolution.LSOA)
    assert sd.data_format == "CSV", (
        f"SourceDataset data format is not CSV, " f"it is {sd.data_format}"
    )
    df = pd.read_csv(sample_csv_filepath)
    assert_frame_equal(sd.data, df)


def test_dataset_csv_forcing_format_no_extra_parameter(sample_csv_filepath):
    from datasets.dataset import DataFormats

    sd = SourceDataset(
        sample_csv_filepath, resolution=DataResolution.LSOA, data_format=DataFormats.CSV
    )
    assert sd.data_format == "CSV", (
        f"SourceDataset data format is not CSV, " f"it is {sd.data_format}"
    )
    df = pd.read_csv(sample_csv_filepath)
    assert_frame_equal(sd.data, df)


def test_dataset_csv_use_cols(sample_csv_filepath):
    # this is the setting for welsh_lsoa_language
    sd = SourceDataset(
        sample_csv_filepath, resolution=DataResolution.LSOA, usecols=[2, 3]
    )
    assert sd.data_format == "CSV", (
        f"SourceDataset data format is not CSV, " f"it is {sd.data_format}"
    )
    df = pd.read_csv(sample_csv_filepath, usecols=[2, 3])
    assert_frame_equal(sd.data, df)


def test_unknown_data_format():
    sd = SourceDataset("non-existing-file", resolution=None)
    assert sd.is_valid is False, "Dataset is valida but it should not."
    assert sd.data is None, "Dataset data content is not None"


def test_unknown_data_forced_data_format():
    from datasets.dataset import DataFormats

    sd = SourceDataset(
        "non-existing-file", resolution=None, data_format=DataFormats.CSV
    )
    assert sd.data is None, "Dataset data is NOT None"

    sd = SourceDataset(
        "non-existing-file",
        resolution=None,
        data_format=DataFormats.CSV,
        usecols=[1, 2],
    )
    assert sd.data is None, "Dataset data is NOT None"


def test_existing_file_with_wrong_imposed_format(sample_csv_filepath):
    from datasets.dataset import DataFormats

    sd = SourceDataset(
        sample_csv_filepath, resolution=DataResolution.LSOA, data_format=DataFormats.XLS
    )
    with pytest.raises(Exception):
        _ = sd.data
        assert sd.data is None, "Data is not None"


def test_source_dataset_with_transform(sample_csv_filepath):
    from transforms import Transpose

    sd = SourceDataset(
        filepath=sample_csv_filepath,
        resolution=DataResolution.LSOA,
        transform=Transpose(),
    )
    assert sd.data is not None
    assert_frame_equal(sd.data, pd.read_csv(sample_csv_filepath).T)
