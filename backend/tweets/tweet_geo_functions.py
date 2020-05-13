# %%
import pandas as pd
import numpy as np
from shapely.geometry import Polygon, Point
from typing import Sequence, Tuple, Union

Lat = float
Long = float
BoundingBox = Sequence[Tuple[Long, Lat]]
MatchingLA = Union[Tuple[str, str, str], pd.DataFrame]
# %%
# def get_laoi(bbox: BoundingBox, la_df: pd.DataFrame, return_all: bool = False)->MatchingLA:
#     """ Get the Intersection Over Union for the the Local Authorities that
#     overlap with the bounding box. Requires 'geometry' col in LA geopandas df.
#     Returns df of local authorities of interest.

#     Parameters
#     ----------
#     bbox: BoundingBox
#         Bounding box coordinates of the tweet

#     la_df: pd.DataFrame
#         (pandas) DataFrame containing information of
#         the Local Authorities (keys) to match

#     return_all: bool
#         Flag controlling whether to return only the top
#         matching local authorities or all of them
#         (ranked by likelihood). By default, False.

#     Returns
#     -------
#     A tuple containing the name, the code, and the reference of
#     the top matching LA, or all of them (in the form of
#     a pandas.DataFrame)
#     """

#     if len(bbox) == 1:
#         # This is the case of using geo.coordinates
#         # for tweets
#         bbox = Point(bbox[0])
#     else:
#         polygon = Polygon(bbox)
#         if not polygon.is_valid:  # Try matching a Point
#             # Apply a slight correction to point coords
#             # to allow for better matching
#             bbox = (np.asarray(bbox) - 0.01)
#             bbox = Point(bbox[0])
#         else:
#             bbox = polygon

#     # Local Authorities of Interest are those that overlap with the bbox
#     laoi = la_df[la_df["geometry"].intersects(bbox)].copy()

#     if (laoi.shape[0] == 0): ## no overlap found
#         return None

#     # Intersection over the union is a measure of how exactly the bounding box and the la overlap
#     laoi["iou"] = la_df["geometry"].apply(
#         lambda g: g.intersection(bbox).area / g.union(bbox).area
#     )
#     # Pop weight is the proportion of the la population covered by the bounding box.
#     laoi["pop_weight"] = (
#         laoi["geometry"].apply(lambda g: (g.intersection(bbox).area / g.area))
#         * laoi["pop"]
#     )
#     # The final likelihood is the IoU multiplied by the population weight
#     laoi["likelihood"] = laoi["iou"] * laoi["pop_weight"]
#     # Sort dataframe by highest to lowest
#     laoi = laoi.sort_values(by="likelihood", ascending=False)

#     if return_all:
#         return laoi
#     return laoi["lad18nm"].iat[0], laoi["lad18cd"].iat[0], laoi["lhb"].iat[0]


# %%
# def add_reference_la(data, la):
#     """ Choose LA with highest likelihood. Add LA and LHB to dataset. """

#     # Get a list of the required values from the first row of sorted dataframe.
#     def laoi_classes(bbox):

#         laoi = get_laoi(bbox, la)
#         if laoi is None:
#             return '', '', ''

#         return laoi["lad18nm"].iat[0], laoi["lad18cd"].iat[0], laoi["lhb"].iat[0]

#     data[["lad18nm", "lad18cd", "lhb"]] = data["bbox_shapely"].apply(laoi_classes)
#     return data


# %%
# In progress - how to define how certain the match is
def class_uncertainty(laoi):
    """ Roughly calculate how certain the classification is based on distances between
    the likelihood of the potentially overlapping LA boundaries. """

    # Sort dataframe by highest to lowest
    laoi = laoi.sort_values(by="likelihood", ascending=False)
    # Get the list of values
    a = laoi["likelihood"]
    a.reset_index().drop()
    del l["index"]

    # If there was only one, the
    if len(a) == 1:
        return 1
    elif len(a) == 2:
        return "only two"  # decide penalty function
    else:
        # Get the difference between each sequential number
        b = a.diff(periods=-1)
        # Divide the distance between the first and second number by the
        b["likelihood"][0] / b[1:].mean()
