import pytest
import pandas as pd
from pandas.testing import assert_frame_equal
from datasets.static_datasets import SourceDataset
from datasets import DataResolution, UnsupportedDataResolution

from datasets.static_datasets import (
    load_language_data,
    load_population_data,
    load_deprivation_data,
    load_population_density_data,
    load_community_cohesion_data,
    load_vulnerability_data,
    load_internet_access_data,
    load_internet_use_data,
    load_ethnicity_data,
)


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
    from datasets.static_datasets import DataFormats

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
    from datasets.static_datasets import DataFormats

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
    from datasets.static_datasets import DataFormats

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


# ----------------------
# Tests: Dataset loading
# ----------------------

# Load Dataset Testing utility function
def load_data_test(load_fn, fixture, extension, data_resolution, **load_fn_params):
    sd = load_fn(**load_fn_params)
    assert sd is not None
    assert sd.data is not None
    assert sd.data_format == extension
    assert sd.resolution is data_resolution
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
        extension="CSV",
        data_resolution=DataResolution.LSOA,
        resolution=DataResolution.LSOA,
    )


def test_load_welsh_language_la(welsh_language_la):
    load_data_test(
        load_fn=load_language_data,
        fixture=welsh_language_la,
        extension="CSV",
        data_resolution=DataResolution.LA,
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
        extension="CSV",
        data_resolution=DataResolution.LA,
        resolution=DataResolution.LA,
    )


def test_load_population_la_over65(welsh_population_la_over65):
    load_data_test(
        load_fn=load_population_data,
        fixture=welsh_population_la_over65,
        extension="CSV",
        data_resolution=DataResolution.LA,
        resolution=DataResolution.LA,
        over_65=True,
    )


def test_load_population_lsoa(welsh_population_lsoa):
    load_data_test(
        load_fn=load_population_data,
        fixture=welsh_population_lsoa,
        extension="CSV",
        data_resolution=DataResolution.LSOA,
        resolution=DataResolution.LSOA,
    )


def test_load_population_lsoa_over65(welsh_population_lsoa_over65):
    load_data_test(
        load_fn=load_population_data,
        fixture=welsh_population_lsoa_over65,
        extension="CSV",
        data_resolution=DataResolution.LSOA,
        resolution=DataResolution.LSOA,
        over_65=True,
    )


#  IMD Data
#  --------
def test_load_deprivation_data_wrong_resolution():
    load_data_test_failure(load_deprivation_data, dataset_name="IMD")


def test_load_deprivation_la(deprivation_la):
    load_data_test(
        load_fn=load_deprivation_data,
        fixture=deprivation_la,
        extension="CSV",
        data_resolution=DataResolution.LA,
        resolution=DataResolution.LA,
    )


def test_load_deprivation_lsoa(deprivation_lsoa):
    load_data_test(
        load_fn=load_deprivation_data,
        fixture=deprivation_lsoa,
        extension="CSV",
        data_resolution=DataResolution.LSOA,
        resolution=DataResolution.LSOA,
    )


#  Population Density Data
#  -----------------------
def test_load_population_density_data_wrong_resolution():
    load_data_test_failure(
        load_population_density_data, dataset_name="Population Density"
    )


def test_load_population_density_la(population_density_la):
    load_data_test(
        load_fn=load_population_density_data,
        fixture=population_density_la,
        extension="CSV",
        data_resolution=DataResolution.LA,
        resolution=DataResolution.LA,
    )


def test_load_population_density_lsoa(population_density_lsoa):
    load_data_test(
        load_fn=load_population_density_data,
        fixture=population_density_lsoa,
        extension="XLSX",
        resolution=DataResolution.LSOA,
        data_resolution=DataResolution.LSOA,
    )


# Vulnerability (LA only)
# -----------------------
def test_load_vulnerability_data(vulnerability_la):
    load_data_test(
        load_fn=load_vulnerability_data,
        fixture=vulnerability_la,
        extension="XLSX",
        data_resolution=DataResolution.LA,
    )


# Community Cohesion (LSOA only)
# -------------------------------
def test_load_community_cohesion_data(community_cohesion_lsoa):
    load_data_test(
        load_fn=load_community_cohesion_data,
        fixture=community_cohesion_lsoa,
        extension="XLSX",
        data_resolution=DataResolution.LA,
    )


# Internet Access and Use (LA only)
# ---------------------------------
def test_load_internet_access_data(internet_access_la):
    load_data_test(
        load_fn=load_internet_access_data,
        fixture=internet_access_la,
        extension="XLSX",
        data_resolution=DataResolution.LA,
    )


def test_load_internet_use_data(internet_use_la):
    load_data_test(
        load_fn=load_internet_use_data,
        fixture=internet_use_la,
        extension="XLSX",
        data_resolution=DataResolution.LA,
    )


#  Ethnicity Data (LA only)
#  ------------------------
def test_load_ethnicity_data(ethnicity_la):
    load_data_test(
        load_fn=load_ethnicity_data,
        fixture=ethnicity_la,
        extension="XLSX",
        data_resolution=DataResolution.LA,
    )
