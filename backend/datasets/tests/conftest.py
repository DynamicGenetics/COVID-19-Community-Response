import os

import pandas as pd
import pytest


# -----------------
# (py)Test Fixtures
# -----------------


@pytest.fixture(scope="session")
def data_folder():
    from datasets import SOURCE_DATA_FOLDER

    return SOURCE_DATA_FOLDER


@pytest.fixture(scope="session")
def sample_csv_filepath(data_folder):
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


@pytest.fixture(scope="function")
def deprivation_la(data_folder):
    csv_fname = "la_WIMD_2019.csv"
    data_fpath = os.path.join(data_folder, csv_fname)
    return pd.read_csv(data_fpath)


@pytest.fixture(scope="function")
def population_density_la(data_folder):
    fname = "la_pop_density_2018.csv"
    data_fpath = os.path.join(data_folder, fname)
    return pd.read_csv(data_fpath, usecols=[1, 11])


@pytest.fixture(scope="function")
def vulnerability_la(data_folder):
    xls_fpath = "la_vulnerableProxy_and_cohesion.xlsx"
    data_fpath = os.path.join(data_folder, xls_fpath)
    df = pd.read_excel(data_fpath, sheet_name="By local authority", usecols="B:X")
    df = df.iloc[[1, 20, 21, 38]].T
    df.reset_index(inplace=True)
    return df.iloc[:, [0, 4]].copy()


@pytest.fixture(scope="function")
def internet_access_la(data_folder):
    fname = "national_survey_internet_use_and_access_la.xlsx"
    data_fpath = os.path.join(data_folder, fname)
    return pd.read_excel(data_fpath, usecols="A,B", skiprows=4, nrows=22)


@pytest.fixture(scope="function")
def internet_use_la(data_folder):
    fname = "national_survey_internet_use_and_access_la.xlsx"
    data_fpath = os.path.join(data_folder, fname)
    return pd.read_excel(data_fpath, usecols="A,B,C", skiprows=34, nrows=22)


@pytest.fixture(scope="function")
def ethnicity_la(data_folder):
    fname = "la_lhb_ethnicity.xlsx"
    data_fpath = os.path.join(data_folder, fname)
    df = pd.read_excel(data_fpath, sheet_name="By Local Authority", usecols="B:X").T
    df.reset_index(inplace=True)
    df.rename(columns=df.iloc[0], inplace=True)
    df.drop(df.index[0], inplace=True)
    df.drop(df.columns[1], axis=1, inplace=True)
    return df


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


@pytest.fixture(scope="function")
def deprivation_lsoa(data_folder):
    fname = "lsoa_IMD_2019.csv"
    data_fpath = os.path.join(data_folder, fname)
    return pd.read_csv(data_fpath)


@pytest.fixture(scope="function")
def population_density_lsoa(data_folder):
    fname = "lsoa_pop_density_2018-19.xlsx"
    data_fpath = os.path.join(data_folder, fname)
    return pd.read_excel(data_fpath, sheet_name=3, usecols="A,B,E", skiprows=4)


@pytest.fixture(scope="function")
def community_cohesion_lsoa(data_folder):
    xls_fpath = "la_vulnerableProxy_and_cohesion.xlsx"
    data_fpath = os.path.join(data_folder, xls_fpath)
    df = pd.read_excel(data_fpath, sheet_name="By local authority", usecols="B:X")
    df = df.iloc[[1, 20, 21, 38]].T
    df.reset_index(inplace=True)
    return df.iloc[:, [0, 2, 3]].copy()
