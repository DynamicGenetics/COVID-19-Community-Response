from shapely.geometry import box, Polygon
from tweet_functions import read_and_tidy, format_bbox
from tweet_geo_functions import get_tweets_loc
import geopandas as gpd
import pandas as pd
import json

# Read in tweets
tweets = read_and_tidy("../../data/nina_7apr.csv")

# Read in LA key
la = gpd.read_file("LA_key.geojson")

# Correctly format the bounding boxes in the dataframe.
tweets = format_bbox(tweets)

# Make a new column with the bounding boxes and shapely objects
tweets["bbox_shapely"] = tweets["place.bounding_box.coordinates"].apply(
    lambda x: Polygon(x[0])
)

# %%
tweets["bbox"] = tweets["bbox_geojson"].apply(lambda c: tuple(map(tuple, c[0][:-1])))

# %%
# Write processed df to pkl for quicker reading in future
pd.to_pickle(tweets, "../data/local/processed_tweets.pkl")

# %%
# Alternative read in from pkl.
tweets = pd.read_pickle("../data/local/processed_tweets.pkl")

# # %%
# ## TESTING - create a smaller tweets df with one row per unique bounding box
# # NB this retains the first occurence of each place name.
# tweets_sm = tweets[~tweets.duplicated(subset='place.full_name')].copy()

# %%
# Read in lsoa key
la = gpd.read_file("lsoa_key.geojson")

# %%
# Collect Unique Coordinates
unique_coords = set(tweets["bbox"].values)


# %%
from functools import partial
from tweet_geo_functions import get_laoi

fetch_laoi = partial(get_laoi, la=la, only_top=True)
laoi_map = {coords: fetch_laoi(coords) for coords in unique_coords}


# %%
# none_coords = list(filter(lambda c: laoi_map[c] is None or laoi_map[c] == ('', '', '')))

# POINTS NOT MATCHED without considering shapely Point object
none_coords = [
    (
        (-3.320704, 51.595735),
        (-3.320704, 51.595735),
        (-3.320704, 51.595735),
        (-3.320704, 51.595735),
    ),
    (
        (-3.18637, 51.50738),
        (-3.18637, 51.50738),
        (-3.18637, 51.50738),
        (-3.18637, 51.50738),
    ),
    (
        (-2.991277, 53.233156),
        (-2.991277, 53.233156),
        (-2.991277, 53.233156),
        (-2.991277, 53.233156),
    ),
    (
        (-3.1641, 51.464774),
        (-3.1641, 51.464774),
        (-3.1641, 51.464774),
        (-3.1641, 51.464774),
    ),
    (
        (-3.190026, 51.507126),
        (-3.190026, 51.507126),
        (-3.190026, 51.507126),
        (-3.190026, 51.507126),
    ),
    (
        (-3.162322, 51.463327),
        (-3.162322, 51.463327),
        (-3.162322, 51.463327),
        (-3.162322, 51.463327),
    ),
    (
        (-3.190722, 51.506496),
        (-3.190722, 51.506496),
        (-3.190722, 51.506496),
        (-3.190722, 51.506496),
    ),
    (
        (-2.836487, 51.588205),
        (-2.836487, 51.588205),
        (-2.836487, 51.588205),
        (-2.836487, 51.588205),
    ),
    (
        (-3.586135, 51.549289),
        (-3.586135, 51.549289),
        (-3.586135, 51.549289),
        (-3.586135, 51.549289),
    ),
]

# %%
from shapely.geometry import Point
import geopandas as gpd
from matplotlib import cm
from matplotlib import pyplot as plt

# %%
# Draw LAs on a map using viridis CMAP
viridis = cm.get_cmap("viridis")

ax = la.geometry.plot(figsize=(15, 15), cmap=viridis)

plt.show()


# %%
import numpy as np

missing_point = np.asarray([-2.991277, 53.233156]) - 0.01

# Draw LAs and centroids on the map
viridis = cm.get_cmap("viridis")

ax = la.geometry.plot(figsize=(15, 15), cmap=viridis)

centroids = la["geometry"].apply(lambda g: list(g.centroid.coords)[0]).values.tolist()
names = la["lad18nm"].values.tolist()
assert len(centroids) == len(names)

for c, name in zip(centroids, names):
    ax.annotate(name, c)

# la.centroids.plot(ax=ax)
ax.scatter(*missing_point, c="r", marker="+")

plt.show()


# %%
ax = la.geometry.plot(figsize=(15, 15))

crs = {"init": "epsg:4326"}
las = list()
points = list()

for c in none_coords:
    match = laoi_map[c]
    if match != ("", "", ""):
        c_gpd = gpd.GeoDataFrame(crs=crs, geometry=[Point(c)])
        points.append((c[0], c_gpd))
        la_m = la[la["lad18nm"] == match[0]]["geometry"].values
        las.append((match[0], gpd.GeoDataFrame(crs=crs, geometry=la_m)))


viridis = cm.get_cmap("viridis", 12)

for i, (name, df) in enumerate(las):
    df.plot(ax=ax, color=viridis.colors[i])
    centroid = list(df["geometry"].values[0].centroid.coords)[0]
    ax.annotate(name, centroid)

for i, (c, df) in enumerate(points):
    # df.plot(ax=ax, color='red')
    ax.annotate(str(i), c, color="r")

plt.show()


# %%
# Mapping bbox to laoi
tweets["lad18nm"], tweets["lad18cd"], tweets["lhb"] = tweets["bbox"].apply(
    lambda c: laoi_map[c]
)

# %%
# Run
tweets2 = get_tweets_loc(tweets_sm, la)

# laoi_example = get_laoi(bbox_tweet, la)

tweets2 = get_tweets_loc(tweets, la)