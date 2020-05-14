import pytest
from pandas.testing import assert_frame_equal
from datasets.dataset import DataResolution, UnsupportedDataResolution

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
