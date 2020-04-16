# %%
import pandas as pd
import json
from typing import Tuple, Callable, List
from abc import ABC, abstractmethod
from functools import partial

Pipe = Tuple[str, Callable[[pd.DataFrame], pd.DataFrame]]


class Pipeline(ABC):
    """ABC implementing the general template of a
    Dynamic Pipeline to process the Twitter dataset.

    The pipeline is composed by a sequence of
    (name, function) pairs.
    Valid (Pipe) functions must comply to the following signature:
        Callable[[pd.DataFrame], pd.DataFrame]
    Therefore, only one parameter is expected, i.e. the dataset
    in the form of a pandas.DataFrame, and a DataFrame is returned
    (to be fed as input for the next step).

    (Concrete) pipeline definitions are obtained via subclassing:
    steps are hard-coded so to have pre-defined and controllable
    behaviours. However, it is always possible to register
    extra steps into a pipeline via the `register` method.
    """

    def __init__(self):
        self._steps = self.create_pipeline()

    @abstractmethod
    def create_pipeline(self) -> List[Pipe]:
        pass

    def register(self, op: Pipe):
        self._steps.append(op)

    def apply(self, data: pd.DataFrame, verbosity: int = 0) -> pd.DataFrame:
        """Executes the pipeline on input data

        Parameters
        ----------
        data : pd.DataFrame
            Input data to initialise the pipeline
        verbosity : int, optional
            Controls the verbosity of the execution of the pipeline,
            by default 0 (no verbosity)

        Returns
        -------
        pd.DataFrame
            New copy of the data after the execution of all the steps
            of the pipeline.
        """
        data_df = data.copy()
        for name, step in self._steps:
            if verbosity > 0:
                print(f'{name} ...', end='')
            data_df = step(data_df)
            if verbosity > 0:
                print('..complete.')
        return data_df


# ---------------------------------
# Pipeline Step (utility) Functions
# ---------------------------------

def _get_welsh_tweets(data: pd.DataFrame, col: str = "place.full_name"):
    """Filters dataframe to only include tweets from Wales,
    by querying on column with place.full_name ('col')."""
    # Filter out non-Wales tweets
    return data[data[col].str.contains("Wales", regex=False, na=False)]


def _create_datetime_index(data: pd.DataFrame) -> pd.DataFrame:
    """ Using the 'created_at' column from a Twitter export,
    makes this the index column in a pandas datetime format. """

    # Parse 'created at' to pandas datetime - requires 'from datetime import datetime'
    data['created_at'] = pd.to_datetime(data["created_at"])
    # Set the datetime of tweet creation as the dataframe index
    data.set_index('created_at', inplace=True)
    return data


def _tidy_text_cols(data: pd.DataFrame,
                    col: str = 'extended_tweet.full_text') -> pd.DataFrame:
    """ Uses values from the short ('text') and extended
    ('extended_tweet.full_text') columns to make a
    single 'text' column with the full version of every tweet. """

    # Keep the data for where 'tweet_full' is not used
    keep = pd.isnull(data[col])
    # Where tweet_full is used, make tweet_full as the text
    data_valid = data[~keep]
    data.loc[~keep, 'text'] = data_valid[col]
    # Drop the (extra) text column
    data.drop(col, axis=1, inplace=True)
    return data


def _bbox_geojson(data: pd.DataFrame, col: str = 'place.bounding_box.coordinates'):
    """ This function will reformat the bounding boxes from strings to lists of lists,
    and will append the first coordinate as the last one to allow for
    geojson conversion."""

    # Convert the lists from strings to json
    data[col] = data[col].apply(lambda x: json.loads(x))

    # Append the first list to the end of the LoL so
    # the coords make a connected shape
    def append_coords(bbox):
        bbox[0].append(bbox[0][0])
        return bbox

    data["bbox_geojson"] = data[col].apply(lambda x: append_coords(x))
    return data


def _bbox_tuple(data: pd.DataFrame) -> pd.DataFrame:
    """Creates a new column in the data with BoundingBoxes encoded as
    tuples of floats (with no repetition). This column is meant
    to ease the processing to match closest local authority.

    NOTE: So far, this Pipe step **must** come after _bbox_geojson
    as it depends on it.
    """
    data["bbox"] = data["bbox_geojson"].apply(lambda c: tuple(map(tuple, c[0][:-1])))
    return data


# %% Twitter Pipeline
class TwitterPipeline(Pipeline):

    def create_pipeline(self) -> List[Pipe]:
        # define pipeline
        filter_welsh = partial(_get_welsh_tweets, col='place.full_name')
        combine_text = partial(_tidy_text_cols, col='extended_tweet.full_text')
        geojson_bbox = partial(
            _bbox_geojson, col='place.bounding_box.coordinates'),

        return [
            ('Filter Tweets from Wales', filter_welsh),
            ('Combine Text fields', combine_text),
            ('Set DateTime Index', _create_datetime_index),
            ('Collect BoundingBox Coordinates (GeoJSON)', geojson_bbox),
            ('Collect BoundingBox Coordinates (Tuples)', _bbox_tuple)
        ]
