"""Python Module to handle data loading"""

# %% - Dataset and Data Map
import os
import pandas as pd
import geopandas as gpd
from warnings import warn
from dataclasses import dataclass


DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), "..", "data")


@dataclass
class Dataset:
    """(Data)Class encapsulating information for a single
    Dataset. Dataset instances will be saved into
    a global DATA_DICTIONARY (see below) acting as a
    proxy to access available datasets.

    This mechanism acts as a surrogate for a Database
    and so potentially subject to change in the future.
    """

    name: str  # dataset unique name
    data_format: str  # format of the data (e.g. CSV, GeoJSON)
    filename: str  # name of the datafile
    sub_dir: str = None  # optional sub-directory of backend/data/static

    @property
    def source_path(self):
        try:  # BTAFTP
            data_path = os.path.join(DATA_FOLDER, self.sub_dir, self.filename)
            with open(data_path) as _:
                pass
        except FileNotFoundError:
            raise FileNotFoundError(f'Data source for "{self.name}" does not exist.')
        else:
            return data_path

    @property
    def is_valid(self):
        try:
            _ = self.source_path
        except FileNotFoundError:
            return False
        else:
            return True

    @property
    def data(self):
        if self.data_format == "csv":
            return pd.read_csv(self.source_path)
        if self.data_format == "geojson":
            return gpd.read_file(self.source_path)
        raise NotImplementedError(f'Data Format for "{self.name}" not yet suported')


# This dictionary maps (local) datasets - identified by unique code-names -
# to their corresponding Dataset.
# This map can be accessed directly, or via specific utility functions,
# which hard-code the data code-name and return the Dataset instance in the map

DATA_MAP = {
    "twitter": Dataset(
        name="Twitter Dataset",
        data_format="csv",
        filename="tweets_dataset.csv",
        sub_dir=os.path.join("live", "raw"),
    ),
    "la_population": Dataset(
        name="Population",
        data_format="csv",
        filename="LA_population_count.csv",
        sub_dir=os.path.join("static", "cleaned"),
    ),
    "la_boundaries": Dataset(
        name="Local Authorities Boundaries",
        data_format="geojson",
        filename="Local_Authority_Districts_(December_2019)_Boundaries_UK_BGC.geojson",
        sub_dir=os.path.join("static", "geoboundaries"),
    ),
    "la_keys": Dataset(
        name="Local Authorities Keys",
        data_format="geojson",
        filename="la_keys.geojson",
        sub_dir=os.path.join("static", "source", "local"),
    ),
    "covid_cases": Dataset(
        name="Covid-19 Cases", data_format="geojson", filename="cases.geojson"
    ),
}


# %% Twitter Dataset
def load_tweets() -> Dataset:
    """Load the Tweets Dataset"""
    tweets = DATA_MAP["twitter"]
    if not tweets.is_valid:
        raise FileNotFoundError("Twitter Dataset cannot be accessed")
    return tweets


# %% Local Authorities
def generate_la_keys(data_filename: str = "la_keys.geojson"):
    """
    Generate the Local Authorities Keys.

    This function merges demographics and buondaries of Local Authorithies
    (as retrieved from "buondaries_LAs.geojson")
    to generate an LA lookup table to be used for a
    quicker geographical location attribution for tweets.
    """

    # Create a version of the static demographics file that
    # we can join with LA data
    la_pop = DATA_MAP["la_population"]
    # Local Authorities Geoobjects
    la_geo = DATA_MAP["la_boundaries"]

    # Merge these to get a geopandas dataframe with population and lhb information
    la_key_df = pd.merge(
        la_geo.data,
        la_pop.data[["lad19cd", "population_count"]],
        on="lad19cd",
        how="inner",
    )
    # Get rid of the (no longer needed) 'id_area' col - it's a duplicate of lad18cd
    # la_key_df.drop("id_area", axis=1, inplace=True)

    la_key_df.to_file(
        os.path.join(
            DATA_FOLDER, DATA_MAP["la_keys"].sub_dir, DATA_MAP["la_keys"].filename
        ),
        driver="GeoJSON",
    )
    warn("Local Authorities Keys data generated!")


def load_local_authorities() -> Dataset:
    """Load the Local Authorities Keys Dataset"""

    la_dataset = DATA_MAP["la_keys"]
    if not la_dataset.is_valid:
        generate_la_keys()
    return la_dataset
