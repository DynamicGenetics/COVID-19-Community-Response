"""Python Module to handle data loading"""

# %% - import
import os
import pandas as pd
import geopandas as gpd
DATA_FOLDER = os.path.join(os.path.abspath(os.path.dirname('__file__')), '..', 'data')

# %%


def load_tweets(data_filename: str, local_dev: bool = False) -> pd.DataFrame:
    """Load the Tweets Data(frame)

    Parameters
    ----------
    data_filename : str
        Name of the Tweets (CSV) file in Data Folder
    local_dev : bool, optional
        Whether loading the data from the local development folder, by default False

    Returns
    -------
    pd.DataFrame
        The Twitter Dataset
    """
    if local_dev:
        data_filepath = os.path.join(DATA_FOLDER, 'local', data_filename)
    else:
        data_filepath = os.path.join(DATA_FOLDER, data_filename)

    try:
        # Read in the data
        tweets = pd.read_csv(data_filepath)
    except FileNotFoundError as e:
        raise e
    else:
        return tweets


# %%
def load_local_authorities() -> gpd.GeoDataFrame:
    """Load the local authorities key dataset as a GeoPandas dataframe
    
    Returns
    -------
    gpd.GeoDataFrame
        Columns: 
    """
    return gpd.read_file("LA_key.geojson")