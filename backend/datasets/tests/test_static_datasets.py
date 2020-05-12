import pytest
import os
import pandas as pd
from pandas.testing import assert_frame_equal
from datasets.static_datasets import SourceDataset
from datasets import DataResolution, UnsupportedDataResolution

from datasets.static_datasets import load_language_data, load_population_data


# -----------------
# (py)Test Fixtures
# -----------------
@pytest.fixture(scope="session")
def data_folder():
    from datasets import SOURCE_DATA_FOLDER

    return SOURCE_DATA_FOLDER


@pytest.fixture(scope="session")
def sample_lsoa_csv_filepath(data_folder):
    csv_filename = "lsoa_welsh_language_2011.csv"
    return os.path.join(data_folder, csv_filename)


# Data Fixture LA Level
# -----------------------
@pytest.fixture(scope="function")
def welsh_language_la(data_folder):
    csv_filename = "la_welsh_frequency_2018-19.csv"
    data_filepath = os.path.join(data_folder, csv_filename)
    return pd.read_csv(data_filepath, usecols=[1, 2, 3, 4])


@pytest.fixture(scope="function")
def welsh_population_la(data_folder):
    csv_filename = "la_population_age_2019.csv"
    data_fpath = os.path.join(data_folder, csv_filename)
    return pd.read_csv(data_fpath, usecols=[3, 15])


@pytest.fixture(scope="function")
def welsh_population_la_over65(data_folder):
    csv_filename = "la_population_age_2019.csv"
    data_fpath = os.path.join(data_folder, csv_filename)
    return pd.read_csv(data_fpath, usecols=[3, 14])


# Data Fixture LSOA Level
# -----------------------
@pytest.fixture(scope="function")
def welsh_language_lsoa(data_folder):
    csv_filename = "lsoa_welsh_language_2011.csv"
    data_filepath = os.path.join(data_folder, csv_filename)
    return pd.read_csv(data_filepath, usecols=[2, 3])


@pytest.fixture(scope="function")
def welsh_population_lsoa(data_folder):
    csv_filename = "lsoa_population_2018_19.csv"
    data_fpath = os.path.join(data_folder, csv_filename)
    return pd.read_csv(data_fpath)


@pytest.fixture(scope="function")
def welsh_population_lsoa_over65(data_folder):
    csv_filename = "lsoa_population_2018_19_over_65.csv"
    data_fpath = os.path.join(data_folder, csv_filename)
    return pd.read_csv(data_fpath)


# -----------------------------
# Tests: SourceDataset creation
# -----------------------------


def test_dataset_csv_no_extra_parameter(sample_lsoa_csv_filepath):
    sd = SourceDataset(sample_lsoa_csv_filepath)
    assert sd.data_format == "CSV", (
        f"SourceDataset data format is not CSV, " f"it is {sd.data_format}"
    )
    df = pd.read_csv(sample_lsoa_csv_filepath)
    assert_frame_equal(sd.data, df)


def test_dataset_csv_forcing_format_no_extra_parameter(sample_lsoa_csv_filepath):
    from datasets.static_datasets import DataFormats

    sd = SourceDataset(sample_lsoa_csv_filepath, data_format=DataFormats.CSV)
    assert sd.data_format == "CSV", (
        f"SourceDataset data format is not CSV, " f"it is {sd.data_format}"
    )
    df = pd.read_csv(sample_lsoa_csv_filepath)
    assert_frame_equal(sd.data, df)


def test_dataset_csv_use_cols(sample_lsoa_csv_filepath):
    # this is the setting for welsh_lsoa_language
    sd = SourceDataset(sample_lsoa_csv_filepath, usecols=[2, 3])
    assert sd.data_format == "CSV", (
        f"SourceDataset data format is not CSV, " f"it is {sd.data_format}"
    )
    df = pd.read_csv(sample_lsoa_csv_filepath, usecols=[2, 3])
    assert_frame_equal(sd.data, df)


def test_unknown_data_format():
    sd = SourceDataset("non-existing-file")
    assert sd.is_valid is False, "Dataset is valida but it should not."
    assert sd.data is None, "Dataset data content is not None"


def test_unknown_data_forced_data_format():
    from datasets.static_datasets import DataFormats

    sd = SourceDataset("non-existing-file", data_format=DataFormats.CSV)
    assert sd.data is None, "Dataset data is NOT None"

    sd = SourceDataset("non-existing-file", data_format=DataFormats.CSV, usecols=[1, 2])
    assert sd.data is None, "Dataset data is NOT None"


def test_existing_file_with_wrong_imposed_format(sample_lsoa_csv_filepath):
    from datasets.static_datasets import DataFormats

    sd = SourceDataset(sample_lsoa_csv_filepath, data_format=DataFormats.XLS)
    with pytest.raises(Exception):
        _ = sd.data
        assert sd.data is None, "Data is not None"


# ----------------------
# Tests: Dataset loading
# ----------------------

# Load Dataset Testing utility function
def load_data_test(load_fn, fixture, format, **load_fn_params):
    sd = load_fn(**load_fn_params)
    assert sd is not None
    assert sd.data is not None
    assert sd.data_format == format
    assert_frame_equal(sd.data, fixture)


def load_data_test_failure(load_fn, dataset_name=""):
    try:
        _ = load_fn(resolution=DataResolution.UKN)
    except UnsupportedDataResolution as e:
        exp_string_low = "unsupported data resolution"
        if dataset_name:
            exp_string_low += f" for {dataset_name.lower()}"
        assert str(e).lower() == exp_string_low, "Different Exception Error"
        assert True
    else:
        assert False

    with pytest.raises(ValueError):
        _ = load_fn(resolution=None)


#  Welsh Language
#  --------------
def test_load_welsh_language_datasets_wrong_resolution():
    load_data_test_failure(load_language_data, dataset_name="Welsh Language")


def test_load_welsh_language_lsoa(welsh_language_lsoa):
    load_data_test(
        load_fn=load_language_data,
        fixture=welsh_language_lsoa,
        format="CSV",
        resolution=DataResolution.LSOA,
    )


def test_load_welsh_language_la(welsh_language_la):
    load_data_test(
        load_fn=load_language_data,
        fixture=welsh_language_la,
        format="CSV",
        resolution=DataResolution.LA,
    )


#  Population Data
#  ---------------


def test_load_population_data_wrong_resolution():
    load_data_test_failure(load_population_data, dataset_name="Welsh Population")


def test_load_population_la(welsh_population_la):
    load_data_test(
        load_fn=load_population_data,
        fixture=welsh_population_la,
        format="CSV",
        resolution=DataResolution.LA,
    )


def test_load_population_la_over65(welsh_population_la_over65):
    load_data_test(
        load_fn=load_population_data,
        fixture=welsh_population_la_over65,
        format="CSV",
        resolution=DataResolution.LA,
        over_65=True,
    )


def test_load_population_lsoa(welsh_population_lsoa):
    load_data_test(
        load_fn=load_population_data,
        fixture=welsh_population_lsoa,
        format="CSV",
        resolution=DataResolution.LSOA,
    )


def test_load_population_lsoa_over65(welsh_population_lsoa_over65):
    load_data_test(
        load_fn=load_population_data,
        fixture=welsh_population_lsoa_over65,
        format="CSV",
        resolution=DataResolution.LSOA,
        over_65=True,
    )
